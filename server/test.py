#!/usr/bin/env python3

import random
import requests

r = random.randint(0, 10000)
url = 'http://127.0.0.1:8080/ocr'
resp = requests.post(url, {
    'email': f'mercisubway{r}@gmail.com',
    'storeNumber': '53994',
    'grade': 10,
    'ticket': r
})
print(resp.status_code)
print(resp.text)
