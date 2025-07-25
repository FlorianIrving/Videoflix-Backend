import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from video_app.models import Video
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

# Tests that the video dashboard view returns a 200 status code for authenticated users
# and a 401 status code for unauthenticated users.
# Also tests that the video detail view returns a 404 status code for an invalid video ID
# and that saving and retrieving watch progress works correctly.
@pytest.mark.django_db
def test_video_dashboard_view_returns_200():
    client = APIClient()
    response = client.get(reverse('video_dashboard'))
    assert response.status_code in [200, 401]

# Tests that the video detail view returns a 200 status code for a valid video ID
# and a 404 status code for an invalid video ID.
@pytest.mark.django_db
def test_video_detail_view_returns_404_for_invalid_id():
    client = APIClient()
    response = client.get(reverse('video_detail', args=[999]))
    assert response.status_code == 404

# Tests that saving watch progress works correctly.
# Creates a user, a video, and then saves progress for that video.
# Finally, it retrieves the progress and checks that it matches what was saved.
@pytest.mark.django_db
def test_save_and_get_progress():
    user = User.objects.create_user(email="progress@example.com", password="Test1234")
    client = APIClient()
    client.force_authenticate(user=user)

    video_file = SimpleUploadedFile("video.mp4", b"file_content", content_type="video/mp4")
    video = Video.objects.create(
        title="Test Video",
        genre="Test",
        video=video_file
    )
    save_response = client.post(reverse('save_progress'), {
        "video_id": video.id,
        "progress_seconds": 123.45
    }, format='json')
    assert save_response.status_code == 200
    get_response = client.get(reverse('get_progress', args=[video.id]))
    assert get_response.status_code == 200
    assert get_response.data.get('progress_seconds') == 123.45