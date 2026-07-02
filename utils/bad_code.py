from rest_framework.exceptions import ValidationError
from datetime import datetime,timedelta,timezone
from crud.auth.base import CRUDSession

BLOCK_DURATION = {
    2:5,
    3:15,
    4:30
}

def increment_invalid_code_attempts(mfa_method:str,crud:CRUDSession,**kwargs) -> ValidationError:
    account = kwargs['account']
    count = account.bad_email_code_count if mfa_method == "email" else account.bad_totp_code_count
    time_now = datetime.now(timezone.utc)

    if count in BLOCK_DURATION:
        block_time = time_now + timedelta(minutes=BLOCK_DURATION[count])

        if count == 4:
            if mfa_method == "email":
                crud.update(db_obj=account, bad_email_code_time=time_now, bad_email_code_count=count+1,
                                 block_time=block_time, is_active=False)

            if mfa_method == "totp":
                pass
            # return send_sms()
            raise ValidationError('Çox sayda səhv parol daxil etmə limiti keçdiyinizə görə hesabınız bloklandı!')

    count += 1

    if mfa_method == "email":
        crud.update(db_obj=account, bad_email_code_time=time_now, bad_email_code_count=count)

    if mfa_method == "totp":
        crud.update(db_obj=account, bad_totp_code_time=time_now, bad_totp_code_count=count)

