import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_password_reset_email_sent():
    User.objects.create_user(email="reset@example.com", password="oldpass123")
    client = APIClient()
    response = client.post(reverse('password_reset'), {"email": "reset@example.com"})
    assert response.status_code in [200, 204]
    assert len(mail.outbox) == 1