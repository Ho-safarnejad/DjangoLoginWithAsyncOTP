from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.user.managers import VerificationCodeManager, AccountManager
from apps.utils.validators import validate_phone


class Account(AbstractUser):
    phone = models.CharField(
        _("phone"), max_length=13, unique=True, validators=[validate_phone]
    )
    username = None
    email = None
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = AccountManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class VerificationCode(models.Model):
    phone = models.CharField(max_length=15, unique=False, null=False, blank=False)
    code = models.IntegerField()
    expiration = models.DateTimeField()
    used = models.BooleanField(default=False)

    objects = VerificationCodeManager()

    class Meta:
        unique_together = ['phone', 'code']
