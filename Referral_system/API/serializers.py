from ..models import ReferralCode, ReferralRelationship

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class ReferralCodeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralCode
        fields = ['user']


class ReferralRelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralRelationship
        fields = ['inviter', 'invited', 'refer_token']
