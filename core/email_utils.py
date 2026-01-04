def extract_username(email):
    return email.split("@")[0]


def extract_domain(email):
    return email.split("@")[1]
