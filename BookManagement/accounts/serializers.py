from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

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
