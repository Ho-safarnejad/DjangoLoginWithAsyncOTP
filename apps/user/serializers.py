from rest_framework.serializers import ModelSerializer

from apps.user.models import VerificationCode
from apps.utils.validators import validate_phone
from apps.user.tasks import send_otp_message


class GetOtpSerializer(ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = '__all__'
        read_only_fields = ('code', 'expiration', 'used')
        extra_kwargs = {

        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        validate_phone(phone)
        return attrs

    def create(self, validated_data):
        otp = VerificationCode.objects.create_otp(**validated_data)
        send_otp_message.delay(otp.phone, otp.code)
        return otp
