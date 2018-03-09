#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify
from jinja2 import Template
import time

app = Flask(__name__, static_url_path='')

@app.route("/")
def idx():
    return render_template('index.html', email=(str(time.time() / 1000) + "@hacktonhub.com"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
