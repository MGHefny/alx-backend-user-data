#!/usr/bin/env python3
""" model user
"""
from models.base import Base


class UserSession(Base):
    """ cls user
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ init fun
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
