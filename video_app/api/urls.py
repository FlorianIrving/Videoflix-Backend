from django.urls import path
from .views import VideoDashboardView, VideoDetailView, SaveProgressView, GetProgressView


urlpatterns = [
    path('', VideoDashboardView.as_view(), name='video_dashboard'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('progress/save/', SaveProgressView.as_view(), name='save_progress'),
    path('progress/<int:video_id>/', GetProgressView.as_view(), name='get_progress'),
]
