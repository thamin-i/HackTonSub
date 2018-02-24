#!/usr/bin/env python3

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
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(msg)
    def do_POST(self):
        try:
            d = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
            args = { key: d[key][0] for key in ['email', 'storeNumber', 'grade', 'ticket'] }
            with closing(ApiHandler()) as api:
                self.send(api.get_cookie_code(**args))
        except RuntimeError as e:
            self.send(e, code=403)
        except Exception as e:
            self.send(repr(e), code=500)

HTTPServer(('', 5002), Serv).serve_forever()
