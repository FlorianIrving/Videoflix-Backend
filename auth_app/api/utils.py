from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

# import jwt
# from datetime import datetime, timedelta

# Sends activation email with uid and token as query params
# Triggered after registration
def send_activation_email(user, request):
    """
    Generates activation link & sends activation email.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    activation_link = f"{settings.FRONTEND_BASE_URL}/pages/auth/activate.html?uid={uid}&token={token}"

    subject = "Activate your account"
    message = f"""
    Hi {user.email},

    Please click the link below to activate your account:

    {activation_link}

    If you did not register, please ignore this email.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
