from rest_framework.request import Request
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from cryptography.fernet import Fernet
from django.conf import settings
import json
from rest_framework.exceptions import ValidationError
from crud.user import user_crud


def send_email_sms(
        request:Request,
        email_type:str,
        **kwargs
):
    if email_type == 'activation':
        try:
            current_site = get_current_site(request)
            # pip install cryptography
            cipher = Fernet(settings.FERNET_KEY.encode())
            user = kwargs['account']

            uid = {
                "username": user.username,
                'email': user.email,
            }

            json_data = json.dumps(uid).encode()
            encrypted_uid = cipher.encrypt(json_data).decode()

            payload = {
                "uid": encrypted_uid,
                "token": default_token_generator.make_token(user)
            }

            signed_payload = signing.dumps(payload)
            protocol = 'https' if request.is_secure() else 'http'

            activation_link = f'{protocol}://{current_site.domain}/accounts/activate/?payload={signed_payload}'

            mail_subject = 'Hesabınızı aktiv edin!'
            message = render_to_string('account/email_activation_sms.html', {
                'user': user,
                "activation_link": activation_link,
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

            limit = int(user.email_code_limit) -1
            user_crud.update(db_obj=user, email_code_limit=limit)

        except Exception as e:
            raise ValidationError({
                "message": f"Email gondermek olmadi: {str(e)}"
            })

    if email_type == 'invoice':
        pass
