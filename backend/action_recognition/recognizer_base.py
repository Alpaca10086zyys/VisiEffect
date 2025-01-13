from abc import ABC, abstractmethod

class ActionRecognizerBase(ABC):
    @abstractmethod
    def recognize_frame(self, frame):
        """
        处理一帧视频并返回识别的动作及其核心坐标。

        :param frame: 当前帧
        :return: 动作的键和坐标 (动作键, 坐标)
        """
        pass
