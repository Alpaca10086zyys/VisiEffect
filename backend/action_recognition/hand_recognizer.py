import cv2
import mediapipe as mp
import math

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult(live)
VisionRunningMode = mp.tasks.vision.RunningMode

# 初始化全局变量，用于存储识别结果
detected_gesture = None

# live:创建回调函数
# def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     global detected_gesture
#     detected_gesture = None
#     gestures = result.gestures
#     for gesture in gestures:
#         for category in gesture:
#             detected_gesture = category.category_name  # 保存当前识别到的手势
#             print(detected_gesture)


# 配置手势识别器的选项
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer0.task'),
    running_mode=VisionRunningMode.VIDEO)
# live:result_callback=print_result)

# 创建手势识别器实例
recognizer = GestureRecognizer.create_from_options(options)


# 基类保持不变
class ActionRecognizerBase:
    def recognize_frame(self, frame):
        raise NotImplementedError


#辅助函数和类定义
def vector_2d_angle(v1, v2):
    """
        求解二维向量的角度
    """
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x * v2_x + v1_y * v2_y) /
                                        (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_


def hand_angle(hand_):
    """
        获取对应手相关向量的二维角度,根据角度确定手势
    """
    angle_list = []
    # ---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- ring 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


def h_gesture(angle_list):
    """
        # 二维约束的方法定义手势
    """
    thr_angle = 65.0
    thr_angle_thumb = 53.0
    thr_angle_s = 49.0
    gesture_str = None
    if 65535.0 not in angle_list:
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "fist"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "bye"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "gun"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "love"
        elif (angle_list[0] > 5) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "ssh"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "666"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
            gesture_str = "three"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "thumbup"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "yeah"
    return gesture_str


class HandRecognizer(ActionRecognizerBase):
    def __init__(self):
        self.timestamp_ms = 0  # 用于视频帧的时间戳
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh  # 添加面部检测模块
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # 支持多只手
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,  # 只检测一个人脸
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )

    # 核心方法：接收一帧图像作为输入（frame），返回识别结果
    def recognize_frame(self, frame):
        # 转为RGB格式
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # wyx：将图像转换为MediaPipe的Image对象
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        # 调用识别器
        self.timestamp_ms += 33  # 假设帧率为30fps，每帧约33ms
        result = recognizer.recognize_for_video(mp_image, self.timestamp_ms)

        global detected_gesture
        detected_gesture = None
        hand_landmarks = None

        # 使用模型：提取识别到的手势名称
        if result.gestures:
            for gesture in result.gestures:
                for category in gesture:
                    detected_gesture = category.category_name  # 保存当前识别到的手势
                    break  # 只获取第一个检测到的手势
            print(f"模型检测到手势: {detected_gesture}")

        # 提取手部关键点
        if result.hand_landmarks:
            for hand in result.hand_landmarks:  # 遍历每只手
                hand_landmarks = hand[0]  # 手部的第一个关键点，即结点 0
                break  # 只处理第一只手
            # print(f"(x,y)为: {hand_landmarks.x,hand_landmarks.y}")

        # 返回手势名称和结点 0 的位置 (x, y)
        if detected_gesture:
            return detected_gesture, (hand_landmarks.x, hand_landmarks.y)
        # else:
        #     return detected_gesture, None

        # ============= 以下是向量部分===============
        frame = cv2.flip(image_rgb, 1)
        results_hands = self.hands.process(frame)
        results_face = self.face_mesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        mouth_open = False  # 初始化嘴巴状态
        left_eye_center = None
        mouth_center = None
        # ----------------- 检测面部 -----------------
        if results_face.multi_face_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                h, w, _ = frame.shape

                # 获取左眼和右眼的中心点
                left_eye_center = (
                    int(face_landmarks.landmark[33].x * w),
                    int(face_landmarks.landmark[33].y * h)
                )
                right_eye_center = (
                    int(face_landmarks.landmark[362].x * w),
                    int(face_landmarks.landmark[362].y * h)
                )

                # 获取嘴巴的中心点
                mouth_upper = (
                    int(face_landmarks.landmark[13].x * w),
                    int(face_landmarks.landmark[13].y * h)
                )
                mouth_lower = (
                    int(face_landmarks.landmark[14].x * w),
                    int(face_landmarks.landmark[14].y * h)
                )
                mouth_center = (
                    (mouth_upper[0] + mouth_lower[0]) // 2,
                    (mouth_upper[1] + mouth_lower[1]) // 2
                )

                # # 绘制眼睛和嘴巴位置
                # cv2.circle(frame, left_eye_center, 5, (0, 255, 0), -1)
                # cv2.circle(frame, right_eye_center, 5, (255, 0, 0), -1)
                # cv2.circle(frame, mouth_center, 5, (0, 255, 255), -1)

        # ----------------- 检测手部 -----------------
        # if detected_gesture:
        #     # 优先模型检测：如果检测到手势，则在图像上显示
        #     cv2.putText(frame, f"Gesture: {detected_gesture}", (50, 50),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        if results_hands.multi_hand_landmarks:
            hands_local = []  # 用于存储2只手的关键点位置
            hand_covering_eye = False  # 手是否遮住了左眼


            for hand_landmarks in results_hands.multi_hand_landmarks:
                # 绘制手部关键点和连接
                # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 存储每只手的关键点位置
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * frame.shape[1]
                    y = hand_landmarks.landmark[i].y * frame.shape[0]
                    hand_local.append((x, y))
                hands_local.append(hand_local)

                # 检查手是否遮住特定部位
                for point in hand_landmarks.landmark:
                    hand_point = (int(point.x * frame.shape[1]), int(point.y * frame.shape[0]))

                    # 检查手是否遮住左眼
                    if left_eye_center and abs(hand_point[0] - left_eye_center[0]) < 30 and abs(
                            hand_point[1] - left_eye_center[1]) < 30:
                        hand_covering_eye = True

                    # 检查手是否遮住嘴巴
                    if mouth_center and abs(hand_point[0] - mouth_center[0]) < 30 and abs(
                            hand_point[1] - mouth_center[1]) < 30:
                        hand_covering_mouth = True

            if hand_covering_eye:
                # 计算手部的包围框 (xmin, ymin, width, height)
                hand_points = hands_local[0]
                xmin = min([point[0] for point in hand_points])
                ymin = min([point[1] for point in hand_points])
                xmax = max([point[0] for point in hand_points])
                ymax = max([point[1] for point in hand_points])
                width = xmax - xmin
                height = ymax - ymin
                # 获取图像的宽高
                frame_height, frame_width = frame.shape[:2]

                # 归一化坐标
                xmin /= frame_width
                ymin /= frame_height
                width /= frame_width
                height /= frame_height
                return "Mowe", (xmin, ymin, width, height)

            elif len(hands_local) == 2:  # 检测到两只手
                # 以下为判断合十
                angle_list0 = hand_angle(hands_local[0])
                angle_list1 = hand_angle(hands_local[1])
                gesture_str0 = h_gesture(angle_list0)
                gesture_str1 = h_gesture(angle_list1)

                # 获取双手的食指指尖坐标（假设食指为index_finger）
                hand1_index_finger = hands_local[0][8]  # 第一个手的食指指尖
                hand2_index_finger = hands_local[1][8]  # 第二个手的食指指尖

                # 计算两只手食指之间的距离
                distance = math.sqrt((hand1_index_finger[0] - hand2_index_finger[0]) ** 2 +
                                     (hand1_index_finger[1] - hand2_index_finger[1]) ** 2)

                # 判断是否合十，距离阈值根据实际场景调整
                if distance < 50 and gesture_str0 == 'gun' and gesture_str1 == 'gun':  # 假设50像素以内为合十状态
                    # 计算双手的总包围框
                    all_points = hands_local[0] + hands_local[1]
                    xmin = min([point[0] for point in all_points])
                    ymin = min([point[1] for point in all_points])
                    xmax = max([point[0] for point in all_points])
                    ymax = max([point[1] for point in all_points])
                    width = xmax - xmin
                    height = ymax - ymin
                    # 获取图像的宽高
                    frame_height, frame_width = frame.shape[:2]

                    # 归一化坐标
                    xmin /= frame_width
                    ymin /= frame_height
                    width /= frame_width
                    height /= frame_height

                    return "grievance", (xmin, ymin, width, height)

            else:  # 单手手势检测
                for hand_local in hands_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)

                    # 计算单手的包围框
                    xmin = min([point[0] for point in hand_local])
                    ymin = min([point[1] for point in hand_local])
                    xmax = max([point[0] for point in hand_local])
                    ymax = max([point[1] for point in hand_local])
                    width = xmax - xmin
                    height = ymax - ymin
                    # 获取图像的宽高
                    frame_height, frame_width = frame.shape[:2]

                    # 归一化坐标
                    xmin /= frame_width
                    ymin /= frame_height
                    width /= frame_width
                    height /= frame_height

                    if gesture_str == "ssh" and mouth_open:
                        return "ssh", (xmin, ymin, width, height)
                    elif gesture_str:
                        return gesture_str, (xmin, ymin, width, height)

        return None,None



