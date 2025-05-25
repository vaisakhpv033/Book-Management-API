from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import re

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT login serializer that prevents blocked users from getting tokens"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adding custom claims to the token
        token["username"] = user.username

        return token

    def validate(self, attrs):
        """Check if user is blocked before generating token"""
        data = super().validate(attrs)
        user = self.user

        if user.is_blocked:
            raise PermissionDenied(
                "Your account has been blocked. Please contact support."
            )

        return data
    
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """Custom JWT refresh serializer to prevent blocked users from refreshing tokens"""

    def validate(self, attrs):
        """Override refresh logic to check if the user is blocked"""

        # get the refresh token from the request and decode it
        refresh_token = attrs["refresh"]
        refresh = RefreshToken(refresh_token)
        user_id = refresh.payload.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            if user.is_blocked:
                raise PermissionDenied(
                    "Your account has been blocked. Please contact support."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist"})

        return super().validate(attrs)



class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "phone_number": {"required": False},
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})
        
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter"})
        
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter"})
        
        if not re.search(r"\d", password):
            raise serializers.ValidationError({"password": "Password must contain at least one number"})

        if not re.search(r"[^\w\s]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character"})

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number", ""),
            password=validated_data["password"],
        )

        return user