from .serializers import UserModelSerializer, ReferralCodeModelSerializer, ReferralRelationshipSerializer
from .permissions import IsOwner
from ..models import ReferralCode, Users, ReferralRelationship

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated


class UserCreateAPIView(generics.CreateAPIView):
    """Возможность регистрации на сайте"""
    serializer_class = UserModelSerializer

    def post(self, request, *args, **kwargs):
        Users(username=self.request.user)
        return Response({"message": f"Пользователь создан"}, status=status.HTTP_201_CREATED)


class ReferralCodeCreateAPIView(generics.CreateAPIView):
    """Создание реферального кода юзером."""
    serializer_class = ReferralCodeModelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = ReferralCode(user=self.request.user)
        code.save()
        return Response({"message": f"Реферальный код создан - {code.code}"}, status=status.HTTP_201_CREATED)


class ReferralCodeDeleteAPIView(generics.DestroyAPIView):
    """Удаление реферального кода юзером."""
    serializer_class = ReferralCodeModelSerializer
    lookup_url_kwarg = "code_id"
    lookup_field = "id"
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        referral_code_instance = ReferralCode.objects.get(user=self.request.user)
        referral_code_instance.delete()
        return Response({"message": "Реферальный код удалён"}, status=status.HTTP_204_NO_CONTENT)


class ReferralCodeListAPIView(generics.ListAPIView):
    """Получения реферального кода по email адресу реферера"""
    serializer_class = ReferralCodeModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        referrer_email = self.request.data.get("referrer_email")
        try:
            user_email = Users.objects.get(email=referrer_email)
        except Users.DoesNotExist:
            raise NotFound(f"Нет зарегистрированного пользователя с адресом '{referrer_email}'")
        id_ = user_email.id
        code = ReferralCode.objects.filter(user_id=id_, is_active=True).values("code")
        return code


class RelationshipInvitedAddAPIView(generics.CreateAPIView):
    """Создание реферальных отношений"""
    serializer_class = ReferralRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request):
        refer_token = self.request.data.get('refer_token')
        try:
            referral_code = ReferralCode.objects.get(code=refer_token)
        except ReferralCode.DoesNotExist:
            raise NotFound(f"Реферальный код '{refer_token}' не найден.")
        code = ReferralCode.objects.get(code=refer_token)
        if not code.is_active:
            raise ValidationError("Реферальный код не активен")

        inviter = referral_code.user
        referral_relationship = ReferralRelationship.objects.create(
            inviter=inviter,
            invited=self.request.user,
            refer_token=referral_code
        )
        referral_relationship.save()
        code.is_active = False
        code.save()
        return Response({"message": "Реферальный код активирован"}, status=status.HTTP_200_OK)


class InvitedesListAPIView(generics.ListAPIView):
    """Список рефералов по id реферера"""
    serializer_class = ReferralRelationshipSerializer
    permission_classes = [IsOwner]
    lookup_url_kwarg = "inviter_id"
    lookup_field = "inviter_id"

    def get_queryset(self):
        return ReferralRelationship.objects.filter(inviter=self.request.user) \
            .select_related("users") \
            .values("invited__username", "invited_id__email") \
            .order_by("invited__username")