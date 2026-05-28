from crud.base import CRUD,ModelType
from datetime import datetime,timedelta,timezone
from typing import Optional

class CRUDSession(CRUD[ModelType]):

    def get_by_username(self, username:str)->Optional[ModelType]:
        try:
            return self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            return None

    def get_by_session(self,session:str)->Optional[ModelType]:
        try:
            return self.model.objects.get(session=session)
        except self.model.DoesNotExist:
            return None

    def get_by_email(self,email:str)->Optional[ModelType]:
        try:
            return self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return None

    def count_recent_by_ip(self, ip_address: str, rate_limit_minutes:int = 1)->int:
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=rate_limit_minutes)

        result = (self.model.objects.filter(
            ip_address=ip_address,
            created_at__gte =cutoff_time)
        ).count()

        return result

    def cleanup_sessions(self,expire_minutes:int | None = None)->int:
        if not expire_minutes:
            expire_minutes = 3

        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=expire_minutes)

        delete_count,_ = self.model.objects.filter(
            created_at__lt=cutoff_time
        ).delete()

        return delete_count   # (deleted_count, details), (5, {'core.Task': 5})