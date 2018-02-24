#!/usr/bin/env python3

import sys
from templates import index
from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__, static_url_path='')

@app.route("/")
def idx():
    return index.main()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
