import cv2
import mediapipe as mp
from .recognizer_base import ActionRecognizerBase


# hyyx： 在此修改
class FaceRecognizer(ActionRecognizerBase):
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.2)

    def recognize_frame(self, frame):
        # 初始化Mediapipe Face模块
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        mp_face_mesh = mp.solutions.face_mesh
        # 初始化Face Detection和Face Mesh模型
        with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
                mp_face_mesh.FaceMesh(min_detection_confidence=0.1, min_tracking_confidence=0.1) as face_mesh:
            # 转为RGB格式
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(image_rgb)
            ####
            # 进行Face Mesh
            results_mesh = face_mesh.process(image_rgb)

            # # 如果检测到面部
            # if results and results.detections:
            #     for detection in results.detections:
            #         mp_drawing.draw_detection(frame, detection)
            if results.detections:
                # 获取识别到的人脸坐标
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box

            # 如果检测到面部并提取到了面部特征点
            if results_mesh and results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    # 面部关键点

                    # 简单的面部表情识别
                    left_lip = face_landmarks.landmark[61]
                    right_lip = face_landmarks.landmark[291]
                    upper_lip = face_landmarks.landmark[13]
                    lower_lip = face_landmarks.landmark[14]
                    lip_height = abs(upper_lip.y - lower_lip.y)
                    lip_width = abs(left_lip.x - right_lip.x)
                    # print("嘴高，嘴宽：", lip_height, lip_width)
                    # print("嘴高/嘴宽：", lip_height / lip_width)
                    # print("右嘴点较左高度差：", right_lip.y - left_lip.y)
                    # 咧嘴笑
                    if lip_height / lip_width > 0.14:
                        mouth = "open"
                    elif lip_height / lip_width > 0.05:
                        mouth = "dudu"
                    elif abs(right_lip.y - left_lip.y) / lip_width > 0.16:
                        mouth = "wai"
                    else:
                        mouth = "Neutral"

                    # 眼部是否闭合的检测
                    # 左眼张开高度
                    left_eyes_height = face_landmarks.landmark[374].y - face_landmarks.landmark[385].y
                    # print("左眼高度:", left_eyes_height)
                    # 左眼宽度
                    left_eyes_width = face_landmarks.landmark[249].x - face_landmarks.landmark[398].x
                    # print("左眼宽度：:", left_eyes_width)
                    # 右眼张开高度
                    right_eyes_height = face_landmarks.landmark[144].y - face_landmarks.landmark[159].y
                    # print("右眼高度:", right_eyes_height)
                    # 右眼宽度
                    right_eyes_width = face_landmarks.landmark[154].x - face_landmarks.landmark[225].x
                    # print("右眼宽度：:", right_eyes_width)

                    # 设定一个阈值，低于该阈值认为眼睛闭合
                    left_threshold = 0.46
                    left_eye_state = "Closed" if left_eyes_height / left_eyes_width < left_threshold else "Open"
                    right_threshold = 0.36
                    right_eye_state = "Closed" if right_eyes_height / right_eyes_width < right_threshold else "Open"

                    # # 在帧上显示眼部状态
                    # cv2.putText(frame, f'Left Eye: {left_eye_state}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # cv2.putText(frame, f'Right Eye: {right_eye_state}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                    #             2)

                    expression = ""
                    # # 在帧上显示嘴部状态
                    # cv2.putText(frame, f'Mouth: {mouth}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    match (mouth, left_eye_state, right_eye_state):
                        case (x, y, z) if x != "wai" and (
                                (y == "Closed" and z == "Open") or (y == "Open" and z == "Closed")):
                            expression = "Wink"
                        case (x, y, z) if (x == "open") and (
                                (y == "Closed" and z == "Closed") or (y == "Open" and z == "Open")):
                            expression = "Grin"
                        case (x, y, z) if (x == "dudu") and (
                                (y == "Closed" and z == "Closed") or (y == "Open" and z == "Open")):
                            expression = "Mwah"
                        case (x, y, z) if (x == "wai") and (y == "Open" and z == "Open"):
                            expression = "Hmph"
                        case _:
                            expression = None

                    # 在帧上显示面部表情
                    # cv2.putText(frame, f'Expression: {expression}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    return expression, (bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height)
            # # 计算FPS
            # frame_count += 1
            # elapsed_time = time.time() - start_time
            # fps = frame_count / elapsed_time
            #
            # # 在帧上显示FPS
            # cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 显示结果
            # cv2.imshow('Facial Expression Analysis', frame)
            ####
            # if results.detections:
            #     # 获取识别到的人脸坐标
            #     for detection in results.detections:
            #         bboxC = detection.location_data.relative_bounding_box
            #         # 返回动作识别的键（如 "face_detected"）和坐标

            return None, None