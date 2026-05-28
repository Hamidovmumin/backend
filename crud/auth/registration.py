from crud.auth.base import CRUDSession
from registration.models import Registration

class CRUDRegistration(CRUDSession[Registration]):
    pass

registration_crud = CRUDRegistration(Registration)