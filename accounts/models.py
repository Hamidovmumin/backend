from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from models.base import BaseDatabaseModel

class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, phone_number, email, password=None)->"Users":
        if not email:
            raise ValueError('The email must be set')
        if not username:
            raise ValueError('The username must be set')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, phone_number, email, password)->"Users":
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin,BaseDatabaseModel):
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # password
    # password sütunu AbstractBaseUser-dən avtomatik gəlir
    password_changed = models.DateTimeField(null=True, blank=True, default=None)
    bad_password_time = models.DateTimeField(null=True, blank=True, default=None)
    bad_password_count = models.IntegerField(default=0)

    block_time = models.DateTimeField(null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20)

    # email
    email = models.EmailField(max_length=250, unique=True)
    email_is_confirmed = models.BooleanField(default=False)
    email_code_limit = models.IntegerField(default=50)
    bad_email_code_time = models.DateTimeField(null=True, blank=True, default=None)
    bad_email_code_count = models.IntegerField(default=0)

    # totp
    totp_token = models.CharField(max_length=256, null=True, blank=True, default=None)
    totp_is_confirmed = models.BooleanField(default=False)
    bad_totp_code_time = models.DateTimeField(null=True, blank=True, default=None)
    bad_totp_code_count = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # is_superuser PermissionsMixin-dən avtomatik gəlir

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # # FIX: is_superuser da yoxlanılır
    # def has_perm(self, perm, obj=None):
    #     if self.is_superuser:
    #         return True
    #     return self.is_admin
    #
    # # FIX: həmişə True qaytarmaq təhlükəlidir
    # def has_module_perms(self, app_label):
    #     if self.is_superuser:
    #         return True
    #     return self.is_admin
