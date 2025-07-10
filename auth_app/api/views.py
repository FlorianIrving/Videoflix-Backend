from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from .utils import send_activation_email, generate_token_for_user
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user, self.request)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Please confirm your email address."},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            return Response({'message': 'Login erfolgreich'}, status=status.HTTP_200_OK)
        else:
            if not User.objects.filter(email=email).exists():
                return Response({'error': 'E-Mail ist nicht registriert'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Passwort ist falsch'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out!"})


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account erfolgreich aktiviert."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Ungültiger oder abgelaufener Token."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Ungültige Aktivierungsdaten."}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"http://dein-frontend/reset/{uidb64}/{token}/"
            send_mail(
                subject="Passwort zurücksetzen",
                message=f"Hier ist dein Link: {reset_url}",
                from_email="noreply@example.com",
                recipient_list=[email],
            )
        return Response({"message": "Wenn ein Konto existiert, wurde eine E-Mail gesendet."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()
        if user and token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Passwort erfolgreich zurückgesetzt"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Ungültiger Link"}, status=status.HTTP_400_BAD_REQUEST)
