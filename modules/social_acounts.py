import requests

SOCIAL_SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}"
}

def find_social_accounts(username):
    results = {}
    for site, url in SOCIAL_SITES.items():
        try:
            r = requests.get(url.format(username), timeout=5)
            if r.status_code == 200:
                results[site] = url.format(username)
        except:
            pass
    return results
