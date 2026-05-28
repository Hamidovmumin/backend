import re

def validate_password_policy(password:str)->str:

    errors = []

    if len(password) < 8:
        errors.append(f"Parol azı 8 simvoldan ibarət olmalıdır!\n") #{settings.password_min_length}

    if not re.search(r'[A-Z]', password):
        errors.append("Parolda böyük hərflərdən istifadə olunmalıdır!")

    # Check lowercase
    if not re.search(r'[a-z]', password):
        errors.append("Parolda böyük hərflərdən istifadə olunmalıdır!")

    # Check digit
    if not re.search(r'\d', password):
        errors.append("Parolda rəqəmlərdən istifadə olunmalıdır!")

    # Check symbol
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/`~;]', password):
        errors.append("Parolda (!@#$%^&* etc.) və s. tipli simvollardan istifadə olunmalıdır!")

    if errors:
        raise ValueError(' '.join(errors))

    return password