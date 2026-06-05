from django.db import models
from models.base import BaseDatabaseModel
from accounts.models import Users
from choices.mfa_choices import MfaChoices


class LoginSession(BaseDatabaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,blank=True)
    password_is_validated = models.BooleanField(default=False)
    mfa_method = models.CharField(choices=MfaChoices.choices,null=True,blank=True)
    email_code = models.CharField(max_length=8,null=True,blank=True)
    code_expire_at = models.DateTimeField(null=True,blank=True)
    email_code_confirmed = models.BooleanField(default=False)
    totp_code_confirmed = models.BooleanField(default=False)
    session = models.CharField(max_length=512, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    uuid = models.UUIDField(null=True, blank=True)
