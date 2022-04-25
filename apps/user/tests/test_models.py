from datetime import timedelta

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.user.models import Account, VerificationCode
from main_app import settings


class AccountModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Account.objects.create(phone='09380502542', first_name='Oveys', last_name='Safarnejad')

    def test_repetitive_phone_is_not_allowed(self):
        self.assertRaises(
            IntegrityError,
            lambda: Account.objects.create(phone='09380502542', first_name='Somebody', last_name='Else')
        )

    def test_invalid_phone_is_not_allowed(self):
        instance = Account(phone='ABC', first_name='Somebody', last_name='Else')
        self.assertRaises(
            ValidationError,
            lambda: instance.full_clean()
        )

    def test_null_attrs_is_not_allowed(self):
        instance = Account(phone='09380502543')
        self.assertRaises(
            ValidationError,
            lambda: instance.full_clean()
        )


class VerificationModelTest(TestCase):

    def setUp(self) -> None:
        VerificationCode.objects.create(phone='09380502542', code=23456, expiration=timezone.now() + timedelta(
            minutes=settings.CODE_EXPIRATION_TIME))
        self.exppired = VerificationCode.objects.create(phone='09380502540', code=34567,
                                                        expiration=timezone.now() - timedelta(
                                                            minutes=settings.CODE_EXPIRATION_TIME))

        self.used = VerificationCode.objects.create(phone='09380502540', code=56789, used=True,
                                                    expiration=timezone.now() + timedelta(
                                                        minutes=60))

        self.valid = VerificationCode.objects.create(phone='09380502540', code=60098, used=False,
                                                     expiration=timezone.now() + timedelta(
                                                         minutes=60))

    def test_unique_together(self):
        """
                Tests unique-together(phone, otp) on VerificationCode model
        """

        self.assertRaises(
            IntegrityError,
            lambda: VerificationCode.objects.create(phone='09380502542', code=23456,
                                                    expiration=timezone.now() + timedelta(
                                                        minutes=settings.CODE_EXPIRATION_TIME))
        )

    def test_remove_expired_code_on_create_otp(self):
        """
                Tests removing expired codes when creating new otp
        """

        VerificationCode.objects.create_otp(phone='09380502540')
        self.assertEqual(1, VerificationCode.objects.filter(phone='09380502540').count())

    def test_remove_used_code_on_create_otp(self):

        """
                        Tests removing unused codes when creating new otp
        """

        VerificationCode.objects.create_otp(phone='09380502540')
        self.assertEqual(1, VerificationCode.objects.filter(phone='09380502540').count())
