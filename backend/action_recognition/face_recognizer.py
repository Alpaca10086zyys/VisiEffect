import cv2
import mediapipe as mp
from .recognizer_base import ActionRecognizerBase


# hyyx： 在此修改
class FaceRecognizer(ActionRecognizerBase):
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.2)

    def recognize_frame(self, frame):
        # 转为RGB格式
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)

        if results.detections:
            # 获取识别到的人脸坐标
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                # 返回动作识别的键（如 "face_detected"）和坐标
                return "face_detected", (bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height)

        return None, None
