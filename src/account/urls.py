from django.contrib import admin
from django.urls import path
from .views import RegisterUserView, UpdateUserProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-profile', UpdateUserProfileView.as_view(), name='update_profile'),
]
