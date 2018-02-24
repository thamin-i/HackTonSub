#!/usr/bin/env python3

import io
import base64
import pyocr
from PIL import Image
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class Serv(BaseHTTPRequestHandler):
    ocr = pyocr.get_available_tools()[0]
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        d = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
        print(d['oui'][0])
        with Image.open(io.BytesIO(base64.b64decode(d['img'][0]))) as img:
            self.wfile.write(Serv.ocr.image_to_string(img).encode())

HTTPServer(('', 8080), Serv).serve_forever()
