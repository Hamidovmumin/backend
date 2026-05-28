from datetime import datetime,timezone

from django.http import HttpRequest
from crud.auth.registration import registration_crud
from crud.auth.base import CRUDSession
from utils.jwt_token import decode_access_token
from django.http import JsonResponse
from utils.ip_address import get_ip

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class SessionTokenAuthentication(BaseAuthentication):
    def __init__(self, crud: CRUDSession):
        self.crud = crud
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("No token provided")
        token = auth_header.split(" ")[1]

        payload = decode_access_token(token)

        session = payload.get('session')
        if not session:
            raise AuthenticationFailed("Invalid token")

        request_ip = get_ip(request)
        token_ip = payload.get('ip_address')

        if request_ip != token_ip:
            raise AuthenticationFailed("IP address uyğun deyil.")

        # token_uuid = payload.get('uuid')
        # if uuid != token_uuid:
        #     raise AuthenticationFailed("Token kecersizdir")

        session_obj = self.crud.get_by_session(session)
        if not session_obj:
            raise AuthenticationFailed("Session not found or expired.")


        return session_obj ,None


class RegistrationAuthentication:
    def __new__(cls):
        return SessionTokenAuthentication(registration_crud)


def _get_session_from_token(
        request: HttpRequest,
        token: str,
        crud: CRUDSession,
):
    payload = decode_access_token(token)

    session = payload.get('session')
    if not session:
        raise ValueError("Session not found")

    request_ip = get_ip(request)
    token_ip = payload.get('ip_address')

    uuid = payload.get('uuid')
    if not uuid:
        raise ValueError("Invalid token payload.")

    if request_ip != token_ip:
        raise ValueError("Invalid token payload.")

    session_obj = crud.get_by_session(session)
    if not session_obj:
        raise ValueError("Session not found or expired.")

    return session_obj




def get_registration_session(request:HttpRequest):
    token = request.COOKIES.get("Authorization")

    return _get_session_from_token(request,token,registration_crud)




