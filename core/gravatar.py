import hashlib
import requests

def gravatar_lookup(email):
    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{h}?d=404"
    r = requests.get(url)
    return url if r.status_code == 200 else None
