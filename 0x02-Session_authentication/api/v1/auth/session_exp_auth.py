#!/usr/bin/env python3
""" model ex authentcation
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """ cls authentcation
    """

    def __init__(self):
        """
        """
        S_D = getenv('SESSION_DURATION')

        try:
            s_d = int(S_D)
        except Exception:
            s_d = 0

        self.s_d = s_d

    def create_session(self, user_id=None):
        """ create user
        """
        x = self.user_id_by_session_id

        s_id = super().create_session(user_id)

        if s_id is None:
            return None

        s_d = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        x[s_id] = s_d

        return s_id

    def user_id_for_session_id(self, session_id=None):
        """ finde user in session
        """

        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        s_d = self.user_id_by_session_id.get(session_id)

        if s_d is None:
            return None

        if self.s_d <= 0:
            return s_d.get('user_id')

        created_at = s_d.get('created_at')

        if created_at is None:
            return None

        ex_time = created_at + timedelta(seconds=self.s_d)

        if ex_time < datetime.now():
            return None

        return s_d.get('user_id')
