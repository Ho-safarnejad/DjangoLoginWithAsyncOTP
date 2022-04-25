from rest_framework.generics import CreateAPIView
from rest_framework.throttling import AnonRateThrottle
from apps.user.serializers import GetOtpSerializer


class GetOtpView(CreateAPIView):
    serializer_class = GetOtpSerializer
    throttle_classes = [AnonRateThrottle]
