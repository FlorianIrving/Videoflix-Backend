from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100)
    video_120p = models.FileField(upload_to='videos/120p/', blank=True, null=True)
    video_360p = models.FileField(upload_to='videos/360p/', blank=True, null=True)
    video_720p = models.FileField(upload_to='videos/720p/', blank=True, null=True)
    video_1080p = models.FileField(upload_to='videos/1080p/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class WatchProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    progress_seconds = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')