from rest_framework.exceptions import ValidationError
from crud.user import user_crud
from crud.auth.base import CRUDSession
from datetime import datetime,timedelta,timezone

BLOCK_DURATION = {
    2:5,
    3:15,
    4:30
}

def handle_failed_login_attempt(account:CRUDSession)->ValidationError:
    block_time =None
    time_now = datetime.now(timezone.utc)
    count = account.bad_password_count

    if count in BLOCK_DURATION:
        block_time = time_now + timedelta(minutes=BLOCK_DURATION[count])

        if count == 4:
            user_crud.update(db_obj=account, bad_password_time=time_now, bad_password_count=count +1,
                             block_time=block_time,is_active=False)
            # return send_sms()
            raise ValidationError('Çox sayda səhv parol daxil etmə limiti keçdiyinizə görə hesabınız bloklandı!')


    count +=1

    user_crud.update(db_obj=account, bad_password_time = time_now ,bad_password_count = count,block_time =block_time)
    raise ValidationError("Daxil edilmiş parol səhvdir")