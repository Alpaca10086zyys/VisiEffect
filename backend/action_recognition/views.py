import cv2
import time
from django.http import JsonResponse
from .action_handler import ActionHandler
from django.views.decorators.csrf import csrf_exempt

# 全局变量控制摄像头状态
camera_active = False


@csrf_exempt
def start_camera(request):
    global camera_active
    if request.method == 'POST':
        if camera_active:
            return JsonResponse({"status": "camera already running"})

        camera_active = True
        cap = cv2.VideoCapture(0)
        action_handler = ActionHandler()
        frame_count = 0  # 帧计数器

        while camera_active:  # 使用全局变量控制循环
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 每隔 20 帧处理一次识别
            if frame_count % 20 == 0:
                action, coordinates = action_handler.process_frame(frame)
                if action is  None or coordinates is  None:
                    continue
                if action and len(coordinates)==4:
                    print(f"Action: {action}, Coordinates: {coordinates}")
                    for scale in range(5, 16):  # 缩放比例从 0.5 到 1.5
                        scale_factor = scale / 10.0
                        offset_y = -int(20 * (scale - 5))  # 位移效果
                        temp_frame = frame.copy()
                        temp_frame = action_handler.draw_sticker(
                            temp_frame, action, coordinates, scale=scale_factor, offset_y=offset_y
                        )
                        cv2.imshow('Action Recognition', temp_frame)
                        if cv2.waitKey(100) & 0xFF == ord('q'):  # 每帧持续 50ms
                            break

            # 实时显示摄像头画面
            cv2.imshow('Action Recognition', frame)

            # 按下 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        camera_active = False
        return JsonResponse({"status": "camera closed"})
    return JsonResponse({"status": "method not allowed"}, status=405)


@csrf_exempt
def stop_camera(request):
    """
    处理关闭摄像头的请求。
    """
    global camera_active
    if request.method == 'POST':
        if camera_active:
            camera_active = False
            return JsonResponse({"status": "stopping camera"})
        else:
            return JsonResponse({"status": "camera not running"}, status=400)
    return JsonResponse({"status": "method not allowed"}, status=405)
