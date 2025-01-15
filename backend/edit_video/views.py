import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from django.conf import settings
from myproject import settings
from action_recognition import hand_recognizer

from action_recognition.action_handler import ActionHandler


@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, video.name)
        with open(file_path, 'wb') as f:
            for chunk in video.chunks():
                f.write(chunk)
        print(f"Video uploaded successfully: {file_path}")

        # 处理视频
        processed_video_url = process_video(file_path)

        if not processed_video_url:
            print("Video processing failed.")
            return JsonResponse({'error': 'Video processing failed'})

        print(f"Processed video URL: {processed_video_url}")
        return JsonResponse({'videoUrl': processed_video_url})

# 视频处理函数
def process_video(file_path):
    # TODO: 在这里添加你的视频处理逻辑（如剪辑、特效等）
    processed_video_path = file_path.replace('uploads', 'processed')  # 处理后视频存储路径
    # 确保处理后目录存在
    processed_video_dir = os.path.dirname(processed_video_path)
    if not os.path.exists(processed_video_dir):
        os.makedirs(processed_video_dir)

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 输出视频的编码
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(processed_video_path, fourcc, fps, (frame_width, frame_height))

    action_handler = ActionHandler()
    frame_count = 0
    action_history = []  # 存储识别的动作，最多保存20帧

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        action, coordinates = action_handler.process_frame(frame)

        # 将当前帧的识别结果加入历史记录
        action_history.append((action, coordinates))
        # 保证只存储最后 20 帧的识别结果
        if len(action_history) > 20:
            action_history.pop(0)

        # 检查最近的 20 帧是否识别出相同的动作
        if len(action_history) == 20 and all(a == action_history[0][0] for a, _ in action_history):
            # 如果连续20帧动作相同，开始粘贴贴纸
            if action not in action_handler.sticker_paths:
                out.write(frame)  # 写入原始帧
                continue

            sticker_path = action_handler.sticker_paths[action]
            sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)  # 读取带透明通道的图片

            # 获取贴图位置和缩放比例
            if coordinates is None or len(coordinates) != 4:
                out.write(frame)  # 写入原始帧
                continue

            # 根据提供的坐标 xmin, ymin, width, height
            xmin, ymin, width, height = coordinates
            # 先将这些坐标转换为整数类型
            xmin = int(xmin * frame_width)  # 将比例转换为像素
            ymin = int(ymin * frame_height)
            width = int(width * frame_width)
            height = int(height * frame_height)

            # 调整贴图大小与目标框的实际像素大小一致
            sticker_resized = cv2.resize(sticker, (width, height))

            # 获取透明通道（如果存在）并创建蒙版
            if sticker_resized.shape[2] == 4:  # 如果图片有透明通道
                alpha_channel = sticker_resized[:, :, 3]
                rgb_image = sticker_resized[:, :, :3]
            else:
                alpha_channel = None
                rgb_image = sticker_resized


            # 现在可以使用这些整数进行切片操作
            overlay = frame[ymin:ymin + height, xmin:xmin + width]

            if alpha_channel is not None:
                # 合并图像，使用透明通道进行合成
                for c in range(0, 3):
                    overlay[:, :, c] = overlay[:, :, c] * (1 - alpha_channel / 255.0) + rgb_image[:, :, c] * (
                                alpha_channel / 255.0)
            else:
                overlay[:] = rgb_image

            # 更新帧
            frame[ymin:ymin + height, xmin:xmin + width] = overlay
            out.write(frame)  # 写入带图片的帧
        else:
            # 如果没有找到一致的动作或还没达到连续20帧，写入原始帧
            out.write(frame)

    cap.release()
    out.release()

    # 生成处理后视频的URL
    processed_video_url = f'http://localhost:8000/media/processed/{os.path.basename(processed_video_path)}'
    return processed_video_url


