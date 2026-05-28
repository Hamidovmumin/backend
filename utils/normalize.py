import re
from typing import Any

def normalize_username(username: Any) -> str:
    errors = []

    if not isinstance(username, str):
        raise ValueError("Username düzgün formatda deyil.")

    username = username.strip()
    if not username:
        errors.append("Username boş ola bilməz.")

    if len(username) < 4:
        errors.append("Username ən azı 4 simvoldan ibarət olmalıdır.")

    if re.search(r"\s", username):
        errors.append("Username daxilində boşluq ola bilməz.")

    if re.search(r"[!@#$%^&*()+\-=\[\]{};:'\",.<>/?\\|`~]", username):
        errors.append("Username-də qadağan olunmuş simvollar var.")

    if errors:
        raise ValueError(' '.join(errors))

    return username.lower()