from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import re


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens.

    This serializer extends the default `TokenObtainPairSerializer` to add custom claims
    to the token and prevent blocked users from obtaining tokens.

    Methods:
        get_token(cls, user): Adds custom claims to the token.
        validate(attrs): Validates the user and checks if the account is blocked.
    """

    @classmethod
    def get_token(cls, user):
        """
        Add custom claims to the token.

        Args:
            user (User): The user instance for which the token is being generated.

        Returns:
            token (RefreshToken): The token with added custom claims.
        """
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        """
        Validate the user and check if the account is blocked.

        Args:
            attrs (dict): The attributes passed for validation.

        Raises:
            PermissionDenied: If the user's account is blocked.

        Returns:
            dict: The validated data.
        """
        data = super().validate(attrs)
        user = self.user

        if user.is_blocked:
            raise PermissionDenied(
                "Your account has been blocked. Please contact support."
            )

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom serializer for refreshing JWT tokens.

    This serializer extends the default `TokenRefreshSerializer` to prevent blocked users
    from refreshing their tokens.

    Methods:
        validate(attrs): Validates the refresh token and checks if the user is blocked.
    """

    def validate(self, attrs):
        """
        Validate the refresh token and check if the user is blocked.

        Args:
            attrs (dict): The attributes passed for validation.

        Raises:
            PermissionDenied: If the user's account is blocked.
            serializers.ValidationError: If the user does not exist.

        Returns:
            dict: The validated data.
        """
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
    """
    Serializer for the User model.

    This serializer handles user creation and validation, including password confirmation
    and password strength checks.

    Attributes:
        confirm_password (CharField): A write-only field for confirming the password.

    Methods:
        validate(data): Validates the user data, including password confirmation and strength.
        create(validated_data): Creates a new user instance.
    """

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
        """
        Validate the user data.

        This method checks if the passwords match and ensures the password meets
        strength requirements (length, uppercase, lowercase, number, special character).

        Args:
            data (dict): The data to validate.

        Raises:
            serializers.ValidationError: If the passwords do not match or fail strength checks.

        Returns:
            dict: The validated data.
        """
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
        """
        Create a new user instance.

        This method removes the `confirm_password` field from the validated data
        and creates a new user using the `create_user` method.

        Args:
            validated_data (dict): The validated data for creating the user.

        Returns:
            User: The created user instance.
        """
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
    

class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model's profile.

    This serializer is used for retrieving and updating the authenticated user's profile.
    It ensures that certain fields, such as the email, are read-only and cannot be modified.

    Attributes:
        email (EmailField): A read-only field to prevent users from modifying their email.

    Meta:
        model (User): The User model associated with this serializer.
        fields (list): The fields to include in the serialized output.

    Fields:
        id (int): The unique identifier of the user (read-only by default).
        username (str): The username of the user.
        email (str): The email address of the user (read-only).
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The phone number of the user.
        profile_picture (str): The URL of the user's profile picture.
        is_blocked (bool): Indicates whether the user is blocked.
    """
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
            "is_blocked",
        ]
