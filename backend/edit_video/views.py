from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from django.conf import settings
from backend.myproject import settings


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

        # 返回视频的 URL
        video_url = f"{settings.MEDIA_URL}uploads/{video.name}"
        return JsonResponse({'videoUrl': video_url})

# 视频处理函数
def process_video(file_path):
    # TODO: 在这里添加你的视频处理逻辑（如剪辑、特效等）
    # 例如：使用 moviepy 进行处理
    processed_video_path = file_path  # 假设处理完后文件路径为 processed_video_path

    # 生成处理后视频的URL
    processed_video_url = f'http://localhost:8000/media/{processed_video_path}'
    return processed_video_url
