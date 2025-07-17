from rest_framework import serializers
from video_app.models import Video


class VideoSerializer(serializers.ModelSerializer):
    hls_paths = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.CharField(source='genre')

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'thumbnail_url', 'created_at', 'hls_paths']

    def get_hls_paths(self, obj):
        base_url = f"/media/hls/{obj.id}"
        return {
            "480p": f"{base_url}/480p/index.m3u8",
            "720p": f"{base_url}/720p/index.m3u8",
            "1080p": f"{base_url}/1080p/index.m3u8",
        }

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        elif obj.thumbnail:
            return obj.thumbnail.url
        return None
    
class VideoListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.CharField(source='genre')

    class Meta:
        model = Video
        fields = ['id', 'title', 'category', 'thumbnail_url', 'created_at']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        elif obj.thumbnail:
            return obj.thumbnail.url
        return None