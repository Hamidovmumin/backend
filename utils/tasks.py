from celery import shared_task

from crud.user import user_crud
from utils.email_sms import send_email_sms


@shared_task
def send_login_security_email(
    user_id: int,
    logout_url: str,
):

    print("LOGIN SECURITY TASK BAŞLADI")
    print("USER ID:", user_id)
    print("LOGOUT URL:", logout_url)

    user = user_crud.get_by_id(
        user_id=user_id
    )

    print("USER:", user)

    if not user:
        print("USER TAPILMADI")
        return

    send_email_sms(
        request=None,
        email_type="login_security",
        user=user,
        logout_url=logout_url,
    )

    print("EMAIL SEND BITDI")