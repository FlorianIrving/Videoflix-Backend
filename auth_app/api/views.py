from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from .utils import send_activation_email, generate_token_for_user
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_token_for_user(user)
            return Response({"token": token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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