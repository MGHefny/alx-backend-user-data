#!/usr/bin/env python3
""" model view session
"""
import os
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from api.v1.app import auth
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ user login
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "password missing"}), 400

    find_user = User.search({'email': email})

    if not find_user:
        return jsonify({"error": "no user found for this email"}), 404

    for x in find_user:
        if not x.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    f_user = find_user[0]
    s_id = auth.create_session(f_user.id)

    c_name = os.getenv('SESSION_NAME')

    res = jsonify(f_user.to_json())
    res.set_cookie(c_name, s_id)

    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """ user logout
    """

    close = auth.destroy_session(request)

    if not close:
        abort(404)

    return jsonify({}), 200
