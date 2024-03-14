from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# api/
urlpatterns = [
    path("create/", views.ReferralCodeCreateAPIView.as_view(), name="create_code"),
    path('register/', views.UserCreateAPIView.as_view(), name="register_users"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
