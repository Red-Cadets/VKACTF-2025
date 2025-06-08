#!/usr/bin/env python3

import requests
import itertools
import sys

if len(sys.argv) > 1:
    user_session = sys.argv[1]
else:
    print("user_session не передан.")
    exit()

url = "https://github.com/ViktPetrov/hack-kollektiv2.0/commit/5"
s = requests.Session()
cookies = {"user_session": f"{user_session}"}

chars = "abcdef0123456789"

for commit in itertools.product(chars, repeat=3):
    prob_commit = ''.join(commit)
    resp = s.get(f"{url}{prob_commit}", cookies=cookies)
    print(f"{url}{prob_commit} {resp.status_code}", end="\r")
    if resp.status_code == 200:
        print(f"FOUND SECRET COMMIT >> {url}{prob_commit}")
        break