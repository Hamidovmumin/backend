from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LoginInformationRequest(serializers.Serializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        errors = {}

        if not attrs['username']:
            errors['username'] = 'username daxil edin!'

        if not attrs['password']:
            errors['password'] = 'şifrəyi daxil edin!'

        if errors:
            raise ValidationError(errors)

        return attrs

class LoginInformationResponse(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.BooleanField()

class LoginMfaResponse(serializers.Serializer):
    masked_email = serializers.CharField(allow_blank=True)
    email = serializers.BooleanField()
    totp = serializers.BooleanField()

class LoginSelectMfaMethodRequest(serializers.Serializer):
    mfa_method = serializers.CharField(allow_blank=True)

class LoginSelectMfaMethodResponse(serializers.Serializer):
    mfa_method = serializers.CharField()

class LoginConfirmEmailCodeRequest(serializers.Serializer):
    code = serializers.CharField(allow_blank=True)

class LoginConfirmEmailCodeResponse(serializers.Serializer):
    code = serializers.BooleanField()

class LoginConfirmTotpCodeRequest(serializers.Serializer):
    totp_code = serializers.CharField(allow_blank=True)

class LoginConfirmTotpCodeResponse(serializers.Serializer):
    totp_code = serializers.BooleanField()