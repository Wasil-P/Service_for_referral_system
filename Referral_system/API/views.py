from .serializers import UserModelSerializer, ReferralCodeModelSerializer, ReferralRelationshipSerializer
from .permissions import IsOwner
from ..models import ReferralCode, Users

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(generics.CreateAPIView):
    """Возможность регистрации на сайте"""

    serializer_class = UserModelSerializer


class ReferralCodeCreateAPIView(generics.CreateAPIView):
    """Создание реферального кода юзером.
    Создание реферальных отношений"""
    serializer_class = ReferralCodeModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReferralCodeDeleteAPIView(generics.DestroyAPIView):
    """Удаление реферального кода юзером."""
    serializer_class = ReferralCodeModelSerializer
    lookup_url_kwarg = "code_id"
    lookup_field = "id"
    permission_classes = [IsOwner]

    def get_queryset(self):
        referral_code_instance = ReferralCode.objects.get(user=self.request.user)
        referral_code_instance.delete()


class ReferralCodeListAPIView(generics.ListAPIView):
    """Получения реферального кода по email адресу реферера"""
    serializer_class = ReferralCodeModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # referrer_email = self.request.query_params.get("bob@gmail.com")
        referrer_email = self.request.GET.get("referrer_email")
        user_with_email = Users.objects.filter(email=referrer_email).first()
        return ReferralCode.objects.filter(user=user_with_email).values("code")


class ReferralRelationshipAddAPIView(generics.CreateAPIView):
    """Установление реферальных отношений"""
    serializer_class = ReferralRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        refer_token = self.request.data.get('refer_token')
        inviter = ReferralCode.objects.get(code=refer_token).user
        # inviter = ReferralCode.objects.filter(code=refer_token).first()
        serializer.save(inviter=inviter,
                        invited=self.request.user,
                        refer_token=refer_token
                        )


