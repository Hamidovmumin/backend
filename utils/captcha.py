import requests
from django.conf import settings

def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"

    response = requests.post(
        url,
        data={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
        },
        timeout=10
    )

    result = response.json()

    return result.get("success", False)