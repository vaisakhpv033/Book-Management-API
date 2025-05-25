from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, RegisterUserView


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterUserView.as_view(), name="register"),
]
