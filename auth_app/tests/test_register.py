import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

# Tests that a user can register successfully.
# Creates a user and then tests that a POST to the registration endpoint
# returns a 201 status code and creates a user with the provided email and password
@pytest.mark.django_db
def test_registration_success():
    client = APIClient()
    response = client.post(reverse('register'), {
        "email": "testuser@example.com",
        "password": "Testpass123!",
        "confirmed_password": "Testpass123!"
    })
    assert response.status_code == 201
    assert User.objects.filter(email="testuser@example.com").exists()