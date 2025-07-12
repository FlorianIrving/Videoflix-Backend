from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

# import jwt
# from datetime import datetime, timedelta


def send_activation_email(user, request):
    """
    Generiert Aktivierungslink & verschickt Aktivierungs-E-Mail.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uid, 'token': token})
    )

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


# def generate_token_for_user(user):
#     """
#     OPTIONAL: JWT oder ein Custom Token generieren.
#     """
#     payload = {
#         'user_id': user.id,
#         'email': user.email,
#         'exp': datetime.utcnow() + timedelta(days=1),
#         'iat': datetime.utcnow(),
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     return token
