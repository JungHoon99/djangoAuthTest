from django.urls import path
from .views import AccountCreateAPIView, LoginAPIView, RefreshTokenAPIView

from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenBlacklistView,
)

app_name = 'accounts'

urlpatterns = [
    path('create/', AccountCreateAPIView.as_view(), name='user_create'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', TokenBlacklistView.as_view(), name='tokenBlacklist'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='tokenRefresh'),
    path('verify/', TokenVerifyView.as_view(), name='tokenVerify'),
]