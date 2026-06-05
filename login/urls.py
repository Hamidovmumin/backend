from django.urls import path
from login.views import (StartSessionView,ValidateInformation,ValidateMfaMethod,SelectMfaMethod,LoginSendEmailCode,
                         LoginConfirmedEmailCode,LoginConfirmedTotpCode,LoginFinish,LogoutAPIView)

urlpatterns = [
    path('1/start/', StartSessionView.as_view(), name='login-start'),
    path('2/validate/information', ValidateInformation.as_view(), name='login-information'),
    path('3/validate/mfa-method',ValidateMfaMethod.as_view(),name='login-validate-mfa-method'),
    path('4/select/mfa-method',SelectMfaMethod.as_view(),name='login-mfa-method'),
    path('5/send/email-code',LoginSendEmailCode.as_view(),name='login-send-email-code'),
    path('6/confirm/email-code',LoginConfirmedEmailCode.as_view(),name='login-confirm-email-code'),
    path('7/confirm/totp-code',LoginConfirmedTotpCode.as_view(),name='login-confirm-totp-code'),
    path('8/finish',LoginFinish.as_view(),name='login-finish'),
    path('9/logout',LogoutAPIView.as_view(),name='login-logout'),
]