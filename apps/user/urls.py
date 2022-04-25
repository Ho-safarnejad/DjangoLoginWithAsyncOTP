from django.urls import path

from apps.user.views import GetOtpView

urlpatterns = [
    path('otp/', GetOtpView.as_view(), name='get-otp'),
]
