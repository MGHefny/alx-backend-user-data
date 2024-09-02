#!/usr/bin/env python3
""" module auth cls
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """ auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ req path auth
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda z: z.strip(), excluded_paths):
                pat = ''
                if exclusion_path[-1] == '*':
                    pat = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pat = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pat = '{}/*'.format(exclusion_path)
                if re.match(pat, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth request
        """
        if request is not None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ user request
        """
        return None
