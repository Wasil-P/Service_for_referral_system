from .serializers import UserModelSerializer, ReferralCodeModelSerializer, ReferralRelationshipSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(generics.CreateAPIView):
    """Возможность регистрации на сайте"""

    serializer_class = UserModelSerializer


class ReferralCodeCreateAPIView(generics.CreateAPIView):
    """Создание реферального кода юзером."""
    serializer_class = ReferralCodeModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReferralRelationshipCreateAPIView(generics.CreateAPIView):
    """Установление реферальных отношений"""
    serializer_class = ReferralRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(inviter=self.request.user)


