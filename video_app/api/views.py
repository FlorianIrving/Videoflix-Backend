from rest_framework.generics import ListAPIView, RetrieveAPIView
from video_app.models import Video
from .serializers import VideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from video_app.models import WatchProgress
from rest_framework.permissions import IsAuthenticated

class VideoDashboardView(ListAPIView):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer

class VideoDetailView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

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
    

class GetProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            progress = WatchProgress.objects.get(user=request.user, video_id=video_id)
            return Response({'progress_seconds': progress.progress_seconds})
        except WatchProgress.DoesNotExist:
            return Response({'progress_seconds': 0})