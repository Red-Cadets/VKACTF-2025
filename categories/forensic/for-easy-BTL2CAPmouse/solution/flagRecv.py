#!/usr/bin/env python3

import requests
import sys
import json

if len(sys.argv) <= 1:
    print("Usage: flagRecv.py <HOST>")
    sys.exit(1)

s = requests.Session()
url = f'http://{sys.argv[1]}:12312/check'
base64NumList=[]
flagCombination = "200125243872242"

with open('base64numbers.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        base64NumList.append(parts[1])

data = {
    "image": f"data:image/png;base64,{base64NumList[0]}"
}

resp = s.post(url,data=data,)
        
for num in flagCombination:
    data = {
        "image": f"data:image/png;base64,{base64NumList[int(num)]}"
    }
    resp = s.post(url,data=data,)
json_output = json.loads(resp.text)
print(json_output["message"])

