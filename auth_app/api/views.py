from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from .utils import send_activation_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


# RegisterView
# - Handles user registration
# - Sends activation email after successful registration
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

# LoginView
# - Authenticates user by email and password
# - Sets JWT tokens as HTTP-only cookies on success
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                {"message": "Login successful."},
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="Lax",
                secure=False,
                path="/",
            )

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="Lax",
                secure=False,
                path="/",
            )

            return response

        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

# LogoutView
# - Invalidates the refresh token
# - Deletes access/refresh cookies
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Token invalid or already blacklisted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

# ActivateView
# - Activates user account via uidb64 and token
# - Triggered by email confirmation link
class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

# RequestPasswordResetView
# - Sends password reset email if user with given email exists
# - Link contains uidb64 and token as query params
class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_BASE_URL}/pages/auth/confirm_password.html?uid={uidb64}&token={token}"
            send_mail(
                subject="Password Reset Request",
                message=f"Here is your password reset link: {reset_url}",
                from_email="noreply@videoflix.de",
                recipient_list=[email],
            )
        return Response({"message": "If an account exists, an email has been sent."}, status=status.HTTP_200_OK)

# PasswordResetConfirmView
# - Validates token and uidb64 from reset link
# - Sets new password if valid and confirmed
class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        token = token.rstrip('/')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link or user"}, status=status.HTTP_400_BAD_REQUEST)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)