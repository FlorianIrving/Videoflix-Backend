from django.urls import path
from .views import VideoDashboardView, VideoDetailView, SaveProgressView, GetProgressView, HLSManifestView, HLSSegmentView


urlpatterns = [
    path('', VideoDashboardView.as_view(), name='video_dashboard'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('progress/save/', SaveProgressView.as_view(), name='save_progress'),
    path('progress/<int:video_id>/', GetProgressView.as_view(), name='get_progress'),
    path('<int:movie_id>/<str:resolution>/index.m3u8', HLSManifestView.as_view()),
    path('<int:movie_id>/<str:resolution>/<str:segment>', HLSSegmentView.as_view()),
]
