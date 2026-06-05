from crud.auth.base import CRUDSession
from login.models import LoginSession

class CRUDRegistration(CRUDSession[LoginSession]):
    pass

login_crud = CRUDRegistration(LoginSession)