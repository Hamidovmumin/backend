from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

pwd_hasher = PasswordHasher(    time_cost=2,
    memory_cost=32768,  # 32 MB
    parallelism=2,)

def get_password_hash(password:str)->str:
    return pwd_hasher.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    try:
        pwd_hasher.verify(hashed_password, plain_password)
        print(pwd_hasher.time_cost)
        print(pwd_hasher.memory_cost)
        print(pwd_hasher.parallelism)
        return True
    except VerifyMismatchError:
        return False
