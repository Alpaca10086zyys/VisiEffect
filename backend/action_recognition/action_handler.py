import cv2
from .face_recognizer import FaceRecognizer
from .hand_recognizer import HandRecognizer
from .pose_recognizer import PoseRecognizer

class ActionHandler:
    def __init__(self):
        self.face_recognizer = FaceRecognizer()
        self.hand_recognizer = HandRecognizer()
        self.pose_recognizer = PoseRecognizer()

    def process_frame(self, frame):
        # 按优先级调用不同的识别器
        action, coordinates = self.face_recognizer.recognize_frame(frame)
        if action:
            return action, coordinates

        action, coordinates = self.hand_recognizer.recognize_frame(frame)
        if action:
            return action, coordinates

        action, coordinates = self.pose_recognizer.recognize_frame(frame)
        if action:
            return action, coordinates

        return None, None

    def draw_result(self, frame, action, coordinates):
        # 根据识别结果画出图像（简单绘制矩形或标记）
        if action == 'face' and coordinates:
            x, y, w, h = int(coordinates.xmin * frame.shape[1]), int(coordinates.ymin * frame.shape[0]), \
                         int(coordinates.width * frame.shape[1]), int(coordinates.height * frame.shape[0])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        elif action == 'hand' and coordinates:
            for landmark in coordinates.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

        elif action == 'pose' and coordinates:
            for landmark in coordinates.landmarks:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

        return frame
