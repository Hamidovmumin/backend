from crud.auth.base import CRUDSession
from accounts.models import Users
from typing import Optional

class CRUDRegistration(CRUDSession[Users]):

    def get_by_username(self, username:str)->Optional[Users]:
        try:
            return self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            return None


user_crud = CRUDRegistration(Users)