from django.urls import path
from registration.views import (StartSessionView,ValidateUsername,
                                ValidateEmail,ValidateTOTP,ConfirmTOTP,
                                ValidatePassword,SendEmailSMS,CreateUser)

urlpatterns = [
    path("1/start/", StartSessionView.as_view(), name="registration-start"),
    path("2/validate/username/", ValidateUsername.as_view(), name="registration-username-validate"),
    path("3/validate/email/", ValidateEmail.as_view(), name="registration-email-validate"),
    path("4/validate/totp/", ValidateTOTP.as_view(), name="registration-totp-validate"),
    path('5/confirm/totp/', ConfirmTOTP.as_view(), name='registration-totp-confirm'),
    path('6/validate/password/', ValidatePassword.as_view(), name='registration-password-validate'),
    path('7/create/user/', CreateUser.as_view(), name='user-create'),
    path('8/activate/email/sms/', SendEmailSMS.as_view(), name='send-email-sms'),
]