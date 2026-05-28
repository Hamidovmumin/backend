from django.db import models
from models.base import BaseDatabaseModel

class Registration(BaseDatabaseModel):
    username = models.CharField(max_length=32,null=True,blank=True)
    first_name = models.CharField(max_length=30,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    password = models.CharField(max_length=512,null=True,blank=True)
    password_is_confirmed = models.BooleanField(default=False)
    email = models.EmailField(max_length=256,null=True,blank=True)
    email_is_confirmed = models.BooleanField(default=False)
    email_sms_expire_at = models.DateTimeField(null=True,blank=True)
    totp_token = models.CharField(max_length=32,null=True,blank=True)
    totp_token_qr_uri = models.CharField(max_length=256,null=True,blank=True)
    totp_is_confirmed = models.BooleanField(default=False)
    session = models.CharField(max_length=512,null=True,blank=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    uuid = models.UUIDField(null=True,blank=True)

    def __str__(self):
        return self.username
