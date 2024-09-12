#!/usr/bin/env python3
""" app flask
"""
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """ main page
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
