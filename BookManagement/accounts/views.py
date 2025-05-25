from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API View for user login.

    """

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    API View for getting new access token.

    """

    serializer_class = CustomTokenRefreshSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    API View for user registration.
    Users will be created in an inactive state until they verify their OTP.

    """

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
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