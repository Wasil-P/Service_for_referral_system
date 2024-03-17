from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""Используйте часть юрл - api/ из пакета Service_for_referral_system модуля urls
    для полного адреса(например - api/relationship/)"""

urlpatterns = [
    path('invitedes/<int:inviter_id>', views.InvitedesListAPIView.as_view(), name="list_invited"),
    path('relationship/', views.RelationshipInvitedAddAPIView.as_view(), name="relationship_add"),
    path('code/', views.ReferralCodeListAPIView.as_view(), name="get_code"),
    path('delete/<int:code_id>', views.ReferralCodeDeleteAPIView.as_view(), name="delete_code"),
    path('create/', views.ReferralCodeCreateAPIView.as_view(), name="create_code"),
    path('register/', views.UserCreateAPIView.as_view(), name="register_users"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
