#!/usr/bin/env python3
""" model basic auth
"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ cls basic auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ base 64 authorize
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        access = authorization_header.split(" ")[-1]
        return access

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ str base decode """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            d_decode = base64_authorization_header.encode('utf-8')
            d_decode = base64.b64decode(d_decode)
            return d_decode.decode('utf-8')
        except Exception:
            return None
