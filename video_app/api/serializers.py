from rest_framework import serializers
from video_app.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'genre',
            'video_120p', 'video_360p', 'video_720p', 'video_1080p',
            'thumbnail', 'created_at'
        ]
