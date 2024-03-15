import random
import string
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


class Users(AbstractUser):
    email = models.EmailField(null=False)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


def validate_date(user):
    existing_active_codes = ReferralCode.objects.filter(user=user, is_active=True)
    if existing_active_codes.exists():
        raise ValidationError("У пользователя уже есть активный ReferralCode.")


def create_expiration_date():
    expiration_date = datetime.now() + timedelta(days=10)
    return expiration_date


def generate_referral_code(length=15):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class ReferralCode(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, validators=[validate_date])
    code = models.CharField(max_length=15, unique=True, default=generate_referral_code)
    expiration_date = models.DateTimeField(default=create_expiration_date)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "code"

    def __str__(self):
        return self.code


class ReferralRelationship(models.Model):
    inviter = models.ForeignKey(Users, related_name='inviter', on_delete=models.CASCADE)
    invited = models.ForeignKey(Users, related_name='invited', on_delete=models.CASCADE, null=True)
    refer_token = models.ForeignKey(ReferralCode, verbose_name="referral_code", on_delete=models.CASCADE)

    class Meta:
        db_table = "relationship"

    def __str__(self):
        return f"{self.inviter}_{self.invited}"


@receiver([post_save], sender=ReferralCode)
def target(sender, instance: ReferralCode, **kwargs):
    referral_code = ReferralCode.objects.get(code=instance.code)
    new_relationship = ReferralRelationship.objects.create(
        inviter=instance.user,
        refer_token=referral_code)
    new_relationship.save()
