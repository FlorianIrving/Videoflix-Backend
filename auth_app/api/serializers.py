from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Serializer for user registration
# - validates matching passwords
# - creates user with email and password
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Serializer for user login
# - authenticates via email and password
# - blocks login for inactive accounts
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account disabled.")
        data['user'] = user
        return data
