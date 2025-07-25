import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_success():
    user = User.objects.create_user(email="login@example.com", password="Testpass123!")
    client = APIClient()
    response = client.post(reverse('login'), {
        "email": "login@example.com",
        "password": "Testpass123!"
    })
    assert response.status_code == 200
    assert response.data["message"] == "Login successful."