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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        return u_mail and u_pass
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        sty = decoded_base64_authorization_header
        u_mail = sty.split(":")[0]
        u_pass = sty[len(u_mail) + 1:]
        return (u_mail, u_pass)
