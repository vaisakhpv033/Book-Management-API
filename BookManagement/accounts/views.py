from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserProfileListSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint for user login.

    This view allows users to obtain a pair of JWT tokens (access and refresh tokens)
    by providing valid credentials (email and password).

    Attributes:
        serializer_class (CustomTokenObtainPairSerializer): The serializer used for token generation.
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    API endpoint for refreshing access tokens.

    This view allows users to obtain a new access token using a valid refresh token.
    It ensures that blocked users cannot refresh their tokens.

    Attributes:
        serializer_class (CustomTokenRefreshSerializer): The serializer used for token refresh.
    """
    serializer_class = CustomTokenRefreshSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    This view allows new users to register by providing their details. 

    Attributes:
        serializer_class (UserSerializer): The serializer used for user creation.
        permission_classes (tuple): Permissions required to access this view. 
                                    Default is `AllowAny`, meaning no authentication is required.

    Methods:
        create(request, *args, **kwargs): Handles the creation of a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.

        This method validates the user data and creates a new user if the data is valid.
        If the data is invalid, it returns an error response.

        Args:
            request (Request): The HTTP request object containing user data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A success response with a status of 201 if the user is created successfully,
                      or an error response with a status of 400 if the data is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.

    This view allows authenticated users to view and update their profile information.
    Users can only access and modify their own profile.

    Attributes:
        permission_classes (list): Permissions required to access this view. 
                                   Default is `IsAuthenticated`, meaning the user must be logged in.
        serializer_class (UserProfileListSerializer): The serializer used for retrieving and updating user profiles.

    Methods:
        get_object(): Retrieves the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileListSerializer

    def get_object(self):
        """
        Retrieve the authenticated user's profile.

        This method returns the user instance associated with the current request.

        Returns:
            User: The authenticated user instance.
        """
        return self.request.user
