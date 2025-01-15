import cv2
import mediapipe as mp
from PIL import Image
import numpy as np
from .recognizer_base import ActionRecognizerBase


# lkx,zy：在此修改
class PoseRecognizer(ActionRecognizerBase):
    def __init__(self):
        # 初始化 mediaPipe
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

    def recognize_frame(self, frame):
        # 初始化Face Detection、Hands和Pose模块
        with self.mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
                self.mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.5) as hands, \
                self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            # 转为RGB格式
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_face = face_detection.process(image_rgb)
            results_hands = hands.process(image_rgb)
            results_pose = pose.process(image_rgb)

            # 手势动作识别（双手张开、双手遮脸、拳头与布）
            if results_hands.multi_hand_landmarks and len(results_hands.multi_hand_landmarks) == 2:
                hand1_landmarks = results_hands.multi_hand_landmarks[0]
                hand2_landmarks = results_hands.multi_hand_landmarks[1]

                # 获取手腕和五个手指的坐标
                hand1_wrist = hand1_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                hand1_thumb = hand1_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                hand1_index = hand1_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                hand1_middle = hand1_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                hand1_ring = hand1_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
                hand1_pinky = hand1_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

                hand2_wrist = hand2_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                hand2_thumb = hand2_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                hand2_index = hand2_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                hand2_middle = hand2_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                hand2_ring = hand2_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
                hand2_pinky = hand2_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

                # 检查手指是否张开（手指tip与wrist的距离是否足够大）
                def is_finger_open(finger_tip, wrist):
                    return abs(finger_tip.x - wrist.x) > 0.1 or abs(finger_tip.y - wrist.y) > 0.1

                # 检查每只手的五个手指是否都张开
                def are_all_fingers_open(hand_landmarks):
                    return (is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
                            is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
                            is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
                            is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
                            is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]))

                # 判断每只手的五个手指是否都张开
                hand1_all_fingers_open = are_all_fingers_open(hand1_landmarks)
                hand2_all_fingers_open = are_all_fingers_open(hand2_landmarks)

                # 判断是否是拳头（所有手指都没有张开）
                def is_fist(hand_landmarks):
                    return not (is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) or
                                is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) or
                                is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) or
                                is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) or
                                is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]))

                hand1_is_fist = is_fist(hand1_landmarks)
                hand2_is_fist = is_fist(hand2_landmarks)

                # 获取手部的区域坐标 (xmin, ymin, xmax, ymax)
                def get_hand_area(hand_landmarks):
                    hand_wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                    hand_thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    hand_pinky = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
                    xmin = min(hand_wrist.x, hand_thumb.x, hand_pinky.x)
                    ymin = min(hand_wrist.y, hand_thumb.y, hand_pinky.y)
                    xmax = max(hand_wrist.x, hand_thumb.x, hand_pinky.x)
                    ymax = max(hand_wrist.y, hand_thumb.y, hand_pinky.y)
                    width = xmax - xmin
                    height = ymax - ymin
                    return xmin, ymin, width, height

                hand1_area = get_hand_area(hand1_landmarks)
                hand2_area = get_hand_area(hand2_landmarks)

                # 判断“拳头和布”的条件
                if (hand1_is_fist and hand2_all_fingers_open) or (hand2_is_fist and hand1_all_fingers_open):
                    if hand1_all_fingers_open:
                        return "firework", hand1_area  # 返回张开手的区域
                    else:
                        return "firework", hand2_area  # 返回张开手的区域

                # 判断手部区域和面部区域是否重叠
                def is_overlap(hand_area, face_area):
                    hand_xmin, hand_ymin, hand_width, hand_height = hand_area
                    face_xmin, face_ymin, face_width, face_height = face_area
                    hand_xmax = hand_xmin + hand_width
                    hand_ymax = hand_ymin + hand_height
                    face_xmax = face_xmin + face_width
                    face_ymax = face_ymin + face_height

                    # 检查矩形是否重叠
                    return not (hand_xmax < face_xmin or hand_xmin > face_xmax or hand_ymax < face_ymin or hand_ymin > face_ymax)

                # 获取面部区域的坐标 (xmin, ymin, width, height)
                face_area = None
                if results_face.detections:
                    face = results_face.detections[0].location_data.relative_bounding_box
                    face_area = (face.xmin, face.ymin, face.width, face.height)

                # 如果两只手都有五个手指张开，并且手部区域与面部区域重叠，则返回 "cover_face"
                if hand1_all_fingers_open and hand2_all_fingers_open:
                    if face_area and (is_overlap(hand1_area, face_area) or is_overlap(hand2_area, face_area)):
                        print("手部遮脸")
                        return "cover_face", hand1_area  # 返回手部区域的坐标格式

                    print("手部不遮脸")
                    return "open_hands", hand1_area  # 返回手部区域的坐标格式

            # 其他动作识别（例如肱二头肌）
            if results_pose.pose_landmarks:
                landmarks = results_pose.pose_landmarks.landmark
                left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
                left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
                right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
                right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
                right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]

                def calculate_angle(a, b, c):
                    angle = np.arctan2(c.y - b.y, c.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x)
                    angle = np.abs(angle)
                    if angle > np.pi:
                        angle = 2 * np.pi - angle
                    return np.degrees(angle)

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                if 70 < left_arm_angle < 95 or 70 < right_arm_angle < 95:
                    # 计算动作范围：返回xmin, ymin, width, height
                    xmin = min(left_shoulder.x, left_elbow.x, left_wrist.x)
                    ymin = min(left_shoulder.y, left_elbow.y, left_wrist.y)
                    xmax = max(left_shoulder.x, left_elbow.x, left_wrist.x)
                    ymax = max(left_shoulder.y, left_elbow.y, left_wrist.y)
                    width = xmax - xmin
                    height = ymax - ymin
                    return "biceps", (xmin, ymin, width, height)

        return None, None


# class PoseRecognizer(ActionRecognizerBase):
#     def __init__(self):
#         # 初始化 mediaPipe
#         self.mp_face_detection = mp.solutions.face_detection
#         self.mp_hands = mp.solutions.hands
#         self.mp_pose = mp.solutions.pose
#         self.mp_drawing = mp.solutions.drawing_utils
#
#     def recognize_frame(self, frame):
#         # 初始化Face Detection、Hands和Pose模块
#         with self.mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
#                 self.mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.5) as hands, \
#                 self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#             # 转为RGB格式
#             image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results_face = face_detection.process(image_rgb)
#             results_hands = hands.process(image_rgb)
#             results_pose = pose.process(image_rgb)
#
#             # 手势动作识别（双手张开、双手遮脸）
#             if results_hands.multi_hand_landmarks and len(results_hands.multi_hand_landmarks) == 2:
#                 hand1_landmarks = results_hands.multi_hand_landmarks[0]
#                 hand2_landmarks = results_hands.multi_hand_landmarks[1]
#
#                 # 获取手腕和五个手指的坐标
#                 hand1_wrist = hand1_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
#                 hand1_thumb = hand1_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
#                 hand1_index = hand1_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
#                 hand1_middle = hand1_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
#                 hand1_ring = hand1_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
#                 hand1_pinky = hand1_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
#
#                 hand2_wrist = hand2_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
#                 hand2_thumb = hand2_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
#                 hand2_index = hand2_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
#                 hand2_middle = hand2_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
#                 hand2_ring = hand2_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
#                 hand2_pinky = hand2_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
#
#                 # 检查手指是否张开（手指tip与wrist的距离是否足够大）
#                 def is_finger_open(finger_tip, wrist):
#                     return abs(finger_tip.x - wrist.x) > 0.1 or abs(finger_tip.y - wrist.y) > 0.1
#
#                 # 检查每只手的五个手指是否都张开
#                 def are_all_fingers_open(hand_landmarks):
#                     return (is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
#                             is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
#                             is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
#                             is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) and
#                             is_finger_open(hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP], hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]))
#
#                 # 判断两只手的五个手指是否都张开
#                 hand1_all_fingers_open = are_all_fingers_open(hand1_landmarks)
#                 hand2_all_fingers_open = are_all_fingers_open(hand2_landmarks)
#
#                 # 获取面部区域的坐标 (xmin, ymin, xmax, ymax)
#                 face_area = None
#                 if results_face.detections:
#                     face = results_face.detections[0].location_data.relative_bounding_box
#                     face_area = (face.xmin, face.ymin, face.width, face.height)
#
#                 # 获取手部的区域坐标 (xmin, ymin, xmax, ymax)
#                 def get_hand_area(hand_landmarks):
#                     hand_wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
#                     hand_thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
#                     hand_pinky = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
#                     xmin = min(hand_wrist.x, hand_thumb.x, hand_pinky.x)
#                     ymin = min(hand_wrist.y, hand_thumb.y, hand_pinky.y)
#                     xmax = max(hand_wrist.x, hand_thumb.x, hand_pinky.x)
#                     ymax = max(hand_wrist.y, hand_thumb.y, hand_pinky.y)
#                     width = xmax - xmin
#                     height = ymax - ymin
#                     return xmin, ymin, width, height
#
#                 hand1_area = get_hand_area(hand1_landmarks)
#                 hand2_area = get_hand_area(hand2_landmarks)
#
#                 # 判断手部区域和面部区域是否重叠
#                 def is_overlap(hand_area, face_area):
#                     hand_xmin, hand_ymin, hand_width, hand_height = hand_area
#                     face_xmin, face_ymin, face_width, face_height = face_area
#                     hand_xmax = hand_xmin + hand_width
#                     hand_ymax = hand_ymin + hand_height
#                     face_xmax = face_xmin + face_width
#                     face_ymax = face_ymin + face_height
#
#                     # 检查矩形是否重叠
#                     return not (hand_xmax < face_xmin or hand_xmin > face_xmax or hand_ymax < face_ymin or hand_ymin > face_ymax)
#
#                 # 如果两只手都有五个手指张开，并且手部区域与面部区域重叠，则返回 "cover_face"
#                 if hand1_all_fingers_open and hand2_all_fingers_open:
#                     if face_area and (is_overlap(hand1_area, face_area) or is_overlap(hand2_area, face_area)):
#                         print("手部遮脸")
#                         return "cover_face", hand1_area  # 返回手部区域的坐标格式
#
#                     print("手部不遮脸")
#                     return "open_hands", hand1_area  # 返回手部区域的坐标格式
#             # 其他动作识别（例如肱二头肌）
#             if results_pose.pose_landmarks:
#                 landmarks = results_pose.pose_landmarks.landmark
#                 left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
#                 right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
#                 right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
#                 right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
#
#                 def calculate_angle(a, b, c):
#                     angle = np.arctan2(c.y - b.y, c.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x)
#                     angle = np.abs(angle)
#                     if angle > np.pi:
#                         angle = 2 * np.pi - angle
#                     return np.degrees(angle)
#
#                 left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
#                 right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
#
#                 if 70 < left_arm_angle < 95 or 70 < right_arm_angle < 95:
#                     # 计算动作范围：返回xmin, ymin, width, height
#                     xmin = min(left_shoulder.x, left_elbow.x, left_wrist.x)
#                     ymin = min(left_shoulder.y, left_elbow.y, left_wrist.y)
#                     xmax = max(left_shoulder.x, left_elbow.x, left_wrist.x)
#                     ymax = max(left_shoulder.y, left_elbow.y, left_wrist.y)
#                     width = xmax - xmin
#                     height = ymax - ymin
#                     return "biceps", (xmin, ymin, width, height)
#         return None, None