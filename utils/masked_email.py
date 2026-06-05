

def masked_email(email:str)->str:
    username ,domain= email.split("@")

    masked_username = username[:3] + "*" * max(0,len(username) - 3)
    masked_domain = "*" * (len(domain) - 1) + domain[-1]

    return f"{masked_username}@{masked_domain}"



