import requests

DEVS = {
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
}

def find_dev_accounts(username):
    results = {}
    for p, url in DEVS.items():
        r = requests.get(url.format(username))
        if r.status_code == 200:
            results[p] = url.format(username)
    return results
