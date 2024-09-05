#!/usr/bin/env python3
""" model session auth
"""
from flask import request

from .auth import Auth


class SessionAuth(Auth):
    """ cls session auth
    """
    pass