from rest_framework.generics import RetrieveAPIView
from video_app.models import Video
from .serializers import VideoSerializer, VideoListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from video_app.models import WatchProgress
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404, FileResponse
from django.conf import settings
import os


# Lists all videos ordered by creation date (DESC)
# Used for the video dashboard
class VideoDashboardView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-created_at')
        serializer = VideoListSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)

# Returns details for a single video by ID
class VideoDetailView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

# Saves the current watch progress for a user and video
class SaveProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        video_id = request.data.get('video_id')
        progress_seconds = request.data.get('progress_seconds')

        video = Video.objects.get(id=video_id)
        progress, created = WatchProgress.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={'progress_seconds': progress_seconds}
        )

        return Response({'message': 'Progress saved!'}, status=status.HTTP_200_OK)

# Returns saved watch progress for a specific video and user
class GetProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            progress = WatchProgress.objects.get(
                user=request.user, video_id=video_id)
            return Response({'progress_seconds': progress.progress_seconds})
        except WatchProgress.DoesNotExist:
            return Response({'progress_seconds': 0})

# Serves the .m3u8 manifest file for HLS video playback
class HLSManifestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id, resolution):
        path = os.path.join(settings.MEDIA_ROOT, f"hls/{movie_id}/{resolution}/index.m3u8")
        print(f"🔍 Trying path: {path}")
        if os.path.exists(path):
            print("Found .m3u8!")
            return FileResponse(open(path, 'rb'), content_type="application/vnd.apple.mpegurl")
        print(".m3u8 NOT FOUND")
        raise Http404("Manifest not found.")

# Serves a specific video segment (.ts) for HLS playback
class HLSSegmentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, movie_id, resolution, segment):
        path = os.path.join(settings.MEDIA_ROOT,
                            f"hls/{movie_id}/{resolution}/{segment}")
        if os.path.exists(path):
            return FileResponse(open(path, 'rb'), content_type="video/MP2T")
        raise Http404("Segment not found.")
