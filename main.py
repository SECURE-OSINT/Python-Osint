#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.email_utils import extract_username, extract_domain
from core.domain import domain_has_mx
from core.gravatar import gravatar_lookup
from modules.social_accounts import find_social_accounts

def main(email):
    username = extract_username(email)
    domain = extract_domain(email)

    print("\nEMAIL:", email)
    print("USERNAME:", username)
    print("DOMAIN ACTIVE:", domain_active(domain))

    avatar = gravatar_lookup(email)
    print("GRAVATAR:", avatar if avatar else "None")

    print("\nFOUND SOCIAL ACCOUNTS:")
    accounts = find_social_accounts(username)
    if accounts:
        for site, url in accounts.items():
            print(f"{site}: {url}")
    else:
        print("None found")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py email@example.com")
        sys.exit(1)

    main(sys.argv[1])
