#!/usr/bin/env python3

import io
import base64
import pyocr
from PIL import Image
from subway import ApiHandler
from contextlib import closing
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class Serv(BaseHTTPRequestHandler):
    ocr = pyocr.get_available_tools()[0]
    def send(self, msg, code=200):
        if not isinstance(msg, bytes):
            if not isinstance(msg, str):
                msg = str(msg)
            msg = msg.encode()
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(msg)
    def do_POST(self):
        d = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
        args = { key: d[key][0] for key in ['email', 'storeNumber', 'grade'] }
        with Image.open(io.BytesIO(base64.b64decode(d['img'][0]))) as img:
            print(Serv.ocr.image_to_string(img).encode())
            ticket = '666'
        try:
            with closing(ApiHandler()) as api:
                self.send(api.get_cookie_code(ticket, **args))
        except RuntimeError as e:
            self.send(e, code=403)

HTTPServer(('', 8080), Serv).serve_forever()
