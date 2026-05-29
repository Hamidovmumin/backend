from crud.auth.base import CRUDSession
from myproject import settings
from utils.generator import generate_string
import uuid
from utils.jwt_token import create_access_token
from datetime import datetime, timedelta, timezone
from rest_framework.request import Request
from rest_framework.exceptions import Throttled
from utils.ip_address import get_ip

class SessionService:
    def start_session(
            self,
            request: Request,
            crud: CRUDSession,
            rate_limit_minutes: int,
            max_attempts:int
    ):
        ip_address = get_ip(request)
        recent_count = crud.count_recent_by_ip(ip_address=ip_address,rate_limit_minutes = rate_limit_minutes)

        if recent_count >= max_attempts:
            raise Throttled(
                detail=f"Too many attempts from this IP. Try again in {rate_limit_minutes} minutes.",
                wait=rate_limit_minutes * 60,
            )

        session_token = generate_string(length=256,digits=True,lowercase=True,uppercase=True)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        device_uuid  = uuid.uuid4()

        crud.create(
            session=session_token,
            ip_address=ip_address,
            uuid=device_uuid,
        )

        access_token = create_access_token(
            data={
                "session": session_token,
                "ip_address": ip_address,
                "uuid": str(device_uuid),
            },
            expires_delta=access_token_expires,
        )

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": str(datetime.now(timezone.utc) + access_token_expires),
        }

session_service = SessionService()



