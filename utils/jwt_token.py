from datetime import timedelta, datetime,timezone
from typing import Any
from myproject.settings import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY,ALGORITHM
import jwt
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed

def create_access_token(
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str)-> str | JsonResponse:
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token muddeti bitmisdir")

    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Not Authenticated")