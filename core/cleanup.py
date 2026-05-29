from crud.auth.base import CRUDSession
from django.db import transaction
from crud.auth.registration import registration_crud
from django.conf import settings

def cleanup_sessions(crud:CRUDSession,model:str):
    try:
        with transaction.atomic():
            count = crud.cleanup_sessions(expire_minutes=settings.SESSION_EXPIRE_MINUTES)
            print(
                f"[Cleanup:{model}] Deleted {count} sessions "
                f"older than {settings.SESSION_EXPIRE_MINUTES} minutes"
            )

    except Exception as e:
        print(f"[Cleanup:{model}] Error: {e}")

def cleanup_expired_registration_sessions():
    return cleanup_sessions(crud=registration_crud, model="Registration")