from crud.auth.registration import registration_crud
from crud.auth.base import CRUDSession
from utils.jwt_token import decode_access_token
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






