import requests

FORUMS = {
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
}

def find_forum_accounts(username):
    found = {}
    for name, url in FORUMS.items():
        r = requests.get(url.format(username))
        if r.status_code == 200:
            found[name] = url.format(username)
    return found
