#!/usr/bin/env python3
""" model session auth
"""
from flask import request
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ cls session auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ user id cls
        """
        x = self.user_id_by_session_id
        if user_id is None or not isinstance(user_id, str):
            return None

        s_id = str(uuid.uuid4())

        x[s_id] = user_id

        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user id by session id
        """
        x = self.user_id_by_session_id
        if session_id is None or not isinstance(session_id, str):
            return None

        return x.get(session_id)

    def current_user(self, request=None) -> User:
        """ user request
        """
        x = self.user_id_for_session_id
        y = self.session_cookie(request)
        u_id = x(y)
        return User.get(u_id)

    def destroy_session(self, request=None):
        """ drop session
        """
        x = self.session_cookie(request)
        y = self.user_id_for_session_id(x)
        if request is None or x is None:
            return False
        if y is None:
            return False
        if x in self.user_id_by_session_id:
            del self.user_id_by_session_id[x]
        return True
