import cv2
import json
from pathlib import Path
from .face_recognizer import FaceRecognizer
from .hand_recognizer import HandRecognizer
from .pose_recognizer import PoseRecognizer

class ActionHandler:
    def __init__(self):
        self.face_recognizer = FaceRecognizer()
        self.hand_recognizer = HandRecognizer()
        self.pose_recognizer = PoseRecognizer()
        self.sticker_paths = self.load_sticker_paths()

    def load_sticker_paths(self):
        # 读取贴纸路径
        with open(Path(__file__).resolve().parent / 'path.json', 'r',encoding="utf-8") as f:
            return json.load(f)

    def process_frame(self, frame):
        # 按优先级调用不同的识别器
        # action, coordinates = self.face_recognizer.recognize_frame(frame)
        # if action:
        #     return action, coordinates
        #
        # action, coordinates = self.hand_recognizer.recognize_frame(frame)
        # if action:
        #     return action, coordinates

        action, coordinates = self.pose_recognizer.recognize_frame(frame)
        if action:
            return action, coordinates

        return None, None

    # def draw_sticker(self, frame, action, coordinates, scale=1.0, offset_y=0):
    #     """根据 action 和坐标绘制贴纸"""
    #     if action not in self.sticker_paths:
    #         return frame
    #
    #     sticker_path = self.sticker_paths[action]
    #     sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)  # 读取带透明通道的图片
    #     if sticker is None:
    #         return frame
    #
    #     # 缩放贴纸
    #     sticker = cv2.resize(sticker, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    #     h, w, _ = sticker.shape
    #
    #     x = int(coordinates[0] * frame.shape[1])  # 宽度方向
    #     y = int(coordinates[1] * frame.shape[0])  # 高度方向
    #     w_box = int(coordinates[2] * frame.shape[1])  # 宽度
    #     h_box = int(coordinates[3] * frame.shape[0])  # 高度
    #     # 获取坐标中心
    #     # x, y, w_box, h_box = (
    #     #     int(coordinates.xmin * frame.shape[1]),
    #     #     int(coordinates.ymin * frame.shape[0]),
    #     #     int(coordinates.width * frame.shape[1]),
    #     #     int(coordinates.height * frame.shape[0]),
    #     # )
    #     center_x, center_y = x + w_box // 2, y + h_box // 2 + offset_y
    #
    #     # 计算贴纸左上角坐标
    #     x1, y1 = center_x - w // 2, center_y - h // 2
    #     x2, y2 = x1 + w, y1 + h
    #
    #     # 确保贴纸不超出帧范围
    #     x1, x2 = max(0, x1), min(frame.shape[1], x2)
    #     y1, y2 = max(0, y1), min(frame.shape[0], y2)
    #
    #     # 叠加贴纸
    #     sticker_h, sticker_w = y2 - y1, x2 - x1
    #     sticker_resized = cv2.resize(sticker, (sticker_w, sticker_h), interpolation=cv2.INTER_AREA)
    #     alpha_s = sticker_resized[:, :, 3] / 255.0
    #     alpha_l = 1.0 - alpha_s
    #
    #     for c in range(3):  # 仅处理 BGR 通道
    #         frame[y1:y2, x1:x2, c] = (
    #             alpha_s * sticker_resized[:, :, c] + alpha_l * frame[y1:y2, x1:x2, c]
    #         )
    #
    #     return frame
    def draw_sticker(self, frame, action, coordinates, scale=1.0, offset_y=0):
        """根据 action 和坐标绘制贴纸"""
        if action not in self.sticker_paths:
            return frame

        sticker_path = self.sticker_paths[action]
        sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)  # 读取带透明通道的图片
        if sticker is None:
            return frame

        # 缩放贴纸
        sticker = cv2.resize(sticker, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        sticker_h, sticker_w, _ = sticker.shape

        x = int(coordinates[0] * frame.shape[1])  # 宽度方向
        y = int(coordinates[1] * frame.shape[0])  # 高度方向
        w_box = int(coordinates[2] * frame.shape[1])  # 宽度
        h_box = int(coordinates[3] * frame.shape[0])  # 高度

        # 获取贴纸中心坐标
        center_x, center_y = x + w_box // 2, y + h_box // 2 + offset_y

        # 计算贴纸左上角和右下角坐标
        x1, y1 = center_x - sticker_w // 2, center_y - sticker_h // 2
        x2, y2 = x1 + sticker_w, y1 + sticker_h

        # 确保贴纸不超出帧范围
        frame_h, frame_w, _ = frame.shape
        x1_new, x2_new = max(0, x1), min(frame_w, x2)
        y1_new, y2_new = max(0, y1), min(frame_h, y2)

        # 计算需要裁剪的贴纸区域
        sticker_x1, sticker_x2 = max(0, -x1), sticker_w - max(0, x2 - frame_w)
        sticker_y1, sticker_y2 = max(0, -y1), sticker_h - max(0, y2 - frame_h)

        # 裁剪贴纸
        sticker_cropped = sticker[sticker_y1:sticker_y2, sticker_x1:sticker_x2]

        # 计算裁剪后的位置
        x1, y1, x2, y2 = x1_new, y1_new, x1_new + sticker_cropped.shape[1], y1_new + sticker_cropped.shape[0]

        # 叠加贴纸
        alpha_s = sticker_cropped[:, :, 3] / 255.0  # 透明度
        alpha_l = 1.0 - alpha_s

        for c in range(3):  # 仅处理 BGR 通道
            frame[y1:y2, x1:x2, c] = (
                    alpha_s * sticker_cropped[:, :, c] + alpha_l * frame[y1:y2, x1:x2, c]
            )

        return frame
