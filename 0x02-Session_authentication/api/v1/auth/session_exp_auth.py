#!/usr/bin/env python3
""" model ex authentcation
"""
import os
import re
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ cls authentcation
    """

    def __init__(self) -> None:
        """ init main fun
        """
        super().__init__()
        s_d = os.getenv('SESSION_DURATION')

        if s_d.isdigit() or (s_d.startswith('-') and s_d[1:].isdigit()):
            self.session_duration = int(s_d)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ finde user in session
        """
        if session_id in self.user_id_by_session_id:
            dc_se = self.user_id_by_session_id[session_id]
            if self.session_duration > 0:
                return None
            if 'created_at' not in dc_se:
                return None
            ex_t = datetime.now()
            s_t = timedelta(seconds=self.session_duration)
            d_t = dc_se['created_at'] + s_t
            if d_t < ex_t:
                return None
            return dc_se['user_id']
