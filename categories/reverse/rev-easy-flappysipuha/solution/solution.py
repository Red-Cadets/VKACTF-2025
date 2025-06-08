#!/usr/bin/env python3

import socket
import base64
import sys

def decrypt_flag(data, key_start=0x42, shift=17):
    current_key = key_start
    decrypted = ""
    for byte in data:
        decrypted_char = byte ^ current_key
        decrypted += chr(decrypted_char)
        current_key = (current_key + shift) % 256
    return decrypted

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <ip>")
        sys.exit(1)
    ip = sys.argv[1]
    port = 9999
    try:
        with socket.create_connection((ip, port)) as sock:
            received = sock.recv(4096).strip()
            print(f"[+] Received (base64): {received.decode()}")
            encrypted_bytes = base64.b64decode(received)
            print(f"[+] Encrypted bytes: {list(encrypted_bytes)}")
            flag = decrypt_flag(encrypted_bytes)
            print(f"[+] Decrypted flag: {flag}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
