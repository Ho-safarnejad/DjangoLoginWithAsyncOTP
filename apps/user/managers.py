from django.db import models
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

import random
from main_app import settings


class AccountManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        user = self.model(phone=phone, first_name=first_name,
                          last_name=last_name, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, first_name, last_name, password, **extra_fields)


class VerificationCodeManager(models.Manager):

    @staticmethod
    def normalize_phone(phone):
        if phone.startswith('0098'):
            return '0' + phone[4:]
        if phone.startswith('+98'):
            return '0' + phone[3:]
        return phone

    @staticmethod
    def create_new_otp():
        random.seed(timezone.now())
        return random.randint(23456, 99999)

    def code_validation(self, phone, code):
        otp = self.filter(code=code, phone=phone, used=False,
                          expiration__gt=timezone.now() - timedelta(
                              minutes=settings.CODE_EXPIRATION_TIME))
        if not otp:
            return False
        otp.update(used=True)
        return True

    def create_otp(self, phone):
        """
            removing used or expired codes
        """
        self.filter(Q(phone=phone, used=True) |
                    Q(phone=phone, expiration__lt=timezone.now() - timedelta(
                        minutes=settings.CODE_EXPIRATION_TIME))) \
            .delete()

        """
            code that is generated in last 120 minutes but not used can be extended.
        """
        valid_codes = self.filter(phone=phone, used=False,
                                  expiration__gt=timezone.now() - timedelta(
                                      minutes=settings.CODE_EXPIRATION_TIME))
        if valid_codes:
            valid_code = valid_codes.first()
            valid_codes.update(expiration=timezone.now() + timedelta(
                minutes=settings.CODE_EXPIRATION_TIME))
            return valid_code
        else:
            code = self.create_new_otp()
            verification_code = self.create(phone=phone, code=code,
                                            expiration=timezone.now() + timedelta(
                                                minutes=settings.CODE_EXPIRATION_TIME))
            return verification_code
