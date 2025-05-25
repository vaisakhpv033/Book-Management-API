from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
