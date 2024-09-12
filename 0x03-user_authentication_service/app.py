#!/usr/bin/env python3
""" app flask
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """ main page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """ user post
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ start log
    """
    email = request.form.get("email")
    password = request.form.get("password")
    session_id = AUTH.create_session(email)
    reply = jsonify({"email": email, "message": "logged in"})
    reply.set_cookie("session_id", session_id)
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        return reply


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ end log
    """
    session_id = request.cookies.get("session_id")
    u = AUTH.get_user_from_session_id(session_id)
    if u is None:
        abort(403)
    AUTH.destroy_session(u.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ user profile
    """
    session_id = request.cookies.get("session_id")
    u = AUTH.get_user_from_session_id(session_id)
    if u is None:
        abort(403)
    return jsonify({"email": u.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ res pass
    """
    email = request.form.get("email")
    res_paw = None
    try:
        res_paw = AUTH.get_reset_password_token(email)
    except ValueError:
        res_paw = None
    if res_paw is None:
        abort(403)
    return jsonify({"email": email, "reset_token": res_paw})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ new pass
    """
    email = request.form.get("email")
    res_paw = request.form.get("reset_token")
    n_paw = request.form.get("new_password")
    state_change = False
    try:
        AUTH.update_password(res_paw, n_paw)
        state_change = True
    except ValueError:
        state_change = False
    if not state_change:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
