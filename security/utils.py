from django.core import signing

def create_login_alert_token(
        user_id:int,
        session_key:str,
) -> str:
    return signing.dumps(
        {
            'user_id': user_id,
            'session_key': session_key,
        },
        salt='login-alert',
    )