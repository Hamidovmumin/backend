from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

pwd_hasher = PasswordHasher()

def get_password_hash(password:str)->str:
    return pwd_hasher.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    try:
        pwd_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
