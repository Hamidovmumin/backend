from rest_framework import serializers
from utils.normalize import normalize_username
from utils.validator import validate_password_policy
from rest_framework.exceptions import ValidationError

class RegistrationUsernameRequest(serializers.Serializer):
    username = serializers.CharField(allow_blank=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        errors = {}

        try:
            attrs['username'] = normalize_username(attrs['username'])
        except ValueError as e:
            errors['username'] = str(e)

        if len(attrs['first_name']) < 3:
            errors['first_name'] = "Ad minimum 3 simvoldan ibarət olmalıdır"

        if len(attrs['last_name']) < 3:
            errors['last_name'] = "Soyad minimum 3 simvoldan ibarət olmalıdır"

        if errors:
            raise ValidationError(errors)

        return attrs

class RegistrationUsernameResponse(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class RegistrationEmailRequest(serializers.Serializer):
    email = serializers.EmailField(allow_blank=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Zəhmət olmasa Email-i daxil edin!')

        try:
            return value
        except ValueError as e:
            raise serializers.ValidationError(str(e))

class RegistrationEmailResponse(serializers.Serializer):
    email = serializers.EmailField()


class RegistrationTOTPResponse(serializers.Serializer):
    totp_token = serializers.CharField()
    totp_token_qr_uri = serializers.CharField()


class RegistrationConfirmTOTPResponse(serializers.Serializer):
    totp_confirm = serializers.BooleanField()

class RegistrationConfirmTOTPRequest(serializers.Serializer):
    totp_code = serializers.CharField()

class RegistrationPasswordRequest(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate_password(self, value):
        try:
            return validate_password_policy(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

class RegistrationPasswordResponse(serializers.Serializer):
    password_confirmed = serializers.BooleanField()


class CreateAccountResponse(serializers.Serializer):
    create_account = serializers.BooleanField()

