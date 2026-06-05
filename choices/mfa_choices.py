from django.db import models
from rest_framework.exceptions import ValidationError

class MfaChoices(models.TextChoices):
    email = 'email'
    totp = 'totp'

def validate_mfa_method(value):
    if value not in MfaChoices.values:
        raise ValidationError("Yanlış MFA tipi")
    return value
