from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)


schema_view = get_schema_view(

    openapi.Info(
        title="Referral_system API",
        default_version="v1",
        description="""
## Здесь вы можете посмотреть API для работы с Referral System
"""
    ),
    patterns=[
        path("api/", include("Referral_system.API.urls")),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ],
    authentication_classes=[
        SessionAuthentication,
        JWTAuthentication,
    ],
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)