import cv2
import mediapipe as mp
from .recognizer_base import ActionRecognizerBase

# wyx,lbb： 在此修改

class HandRecognizer(ActionRecognizerBase):
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def recognize_frame(self, frame):
        # 转为RGB格式
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 获取手部的位置（例如，使用第一个手指的坐标）
                x, y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x, \
                    hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y
                # 返回动作识别的键和坐标
                return "hand_detected", (x, y)

        return None, None