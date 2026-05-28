from crud.auth.base import CRUDSession
from django.db import transaction
from crud.auth.registration import registration_crud

def cleanup_sessions(crud:CRUDSession,model:str):
    try:
        with transaction.atomic():
            count = crud.cleanup_sessions(expire_minutes=30)
            print(
                f"[Cleanup:{model}] Deleted {count} sessions "
                f"older than 30 minutes"
            )

    except Exception as e:
        print(f"[Cleanup:{model}] Error: {e}")

def cleanup_expired_registration_sessions():
    return cleanup_sessions(crud=registration_crud, model="Registration")