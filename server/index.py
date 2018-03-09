#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__, static_url_path='')

@app.route("/")
def idx():
    return "Subway generator here"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
