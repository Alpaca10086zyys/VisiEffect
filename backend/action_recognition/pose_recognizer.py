import cv2
import mediapipe as mp
from .recognizer_base import ActionRecognizerBase

# lkx,zy:在此修改
class PoseRecognizer(ActionRecognizerBase):
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def recognize_frame(self, frame):
        # 转为RGB格式
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            # 获取人体关键点坐标（例如，肩膀位置）
            shoulder = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 返回动作识别的键和坐标
            return "pose_detected", (shoulder.x, shoulder.y)

        return None, None