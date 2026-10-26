from rest_framework.request import Request
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from cryptography.fernet import Fernet
from django.conf import settings
import json
from rest_framework.exceptions import ValidationError
from crud.user import user_crud
from crud.auth.login import login_crud
from utils.generator import generate_string
from datetime import datetime,timedelta,timezone

def send_email_sms(
        request:Request | None,
        email_type:str,
        **kwargs
):
    if email_type == 'activation':
        try:
            current_site = get_current_site(request)

            cipher = Fernet(settings.FERNET_KEY.encode())
            user = kwargs['account']

            uid = {
                "username": user.username,
                "email": user.email,
            }

            json_data = json.dumps(uid).encode()
            encrypted_uid = cipher.encrypt(json_data).decode()

            payload = {
                "uid": encrypted_uid,
                "token": default_token_generator.make_token(user)
            }

            signed_payload = signing.dumps(payload)
            protocol = 'https' if request.is_secure() else 'http'

            activation_link = (
                f'{protocol}://{current_site.domain}'
                f'/accounts/activate/?payload={signed_payload}'
            )

            mail_subject = 'Hesabınızı aktiv edin!'

            html_message = render_to_string(
                'account/email_activation_sms.html',
                {
                    'user': user,
                    'activation_link': activation_link,
                }
            )

            send_email = EmailMultiAlternatives(
                subject=mail_subject,
                body="Hesabınızı aktivləşdirmək üçün emaildəki linkə daxil olun.",
                to=[user.email],
            )
            send_email.attach_alternative(
                html_message,
                "text/html"
            )
            send_email.send()

            limit = int(user.email_code_limit) - 1
            user_crud.update(
                db_obj=user,
                email_code_limit=limit
            )

        except Exception as e:
            raise ValidationError({
                "message": f"Email gondermek olmadi: {str(e)}"
            })

    if email_type == 'invoice':
        pass

    if email_type == 'mfa_code':
        try:
            code = generate_string(length=6, digits=True)

            login_session = kwargs['account']

            code_expire_at = (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=15)
            )

            login_crud.update(
                db_obj=login_session,
                email_code=code,
                code_expire_at=code_expire_at
            )

            mail_subject = 'Doğrulama kodunuz!'

            html_message = render_to_string(
                'security/login_email_code.html',
                {
                    "code": code,
                }
            )

            send_email = EmailMultiAlternatives(
                subject=mail_subject,
                body='Sizin doğrulama kodunuz',
                to=[login_session.user.email],
            )

            send_email.attach_alternative(
                html_message,
                "text/html"
            )

            send_email.send()

            limit = int(login_session.user.email_code_limit) - 1

            user_crud.update(
                db_obj=login_session.user,
                email_code_limit=limit
            )

        except Exception as e:
            raise ValidationError({
                "message": f"Email gondermek olmadi: {str(e)}"
            })

    if email_type == 'login_security':

        html_message = render_to_string(
            'security/login_alert.html',
            {
                'user': kwargs['user'],
                'logout_url': kwargs['logout_url']
            }
        )

        email = EmailMultiAlternatives(
            subject="Hesabınıza yeni giriş edildi",
            body=(
                "Hesabınıza yeni giriş edildi. "
                "Əgər bu siz deyilsinizsə hesabdan çıxın."
            ),
            to=[kwargs['user'].email],
        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send()


