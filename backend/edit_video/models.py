from django.db import models

class VideoTask(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    video_file = models.FileField(upload_to='videos/')
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
