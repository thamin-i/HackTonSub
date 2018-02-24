#!/usr/bin/env python3

import requests
import base64

url = 'http://127.0.0.1:8080/ocr'
with open('/tmp/img.png', 'rb') as img:
    print(requests.post(url, {
        'oui': 'non',
        'img': base64.b64encode(img.read())
    }).text)
