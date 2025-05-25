from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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