#!/usr/bin/env python3
""" auth model
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User


def _hash_password(password: str) -> str:
    """ hash pass
    """
    x = password.encode("utf-8")
    y = bcrypt.gensalt()
    encript_paw = bcrypt.hashpw(x, y)
    return encript_paw


def _generate_uuid() -> str:
    """ uuid generate
    """
    UUID = uuid4()
    return str(UUID)


class Auth:
    """ auth cls
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ login user
        """
        x = self._db
        try:
            u = x.find_user_by(email=email)
        except NoResultFound:
            hash_paw = _hash_password(password)
            u = x.add_user(email, hash_paw)
            return u
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ login valid
        """
        x = self._db
        try:
            u = x.find_user_by(email=email)
        except NoResultFound:
            return False
        u_paw = u.hashed_password
        hash_paw = password.encode("utf-8")
        if bcrypt.checkpw(hash_paw, u_paw):
            return True
        return False

    def create_session(self, email: str) -> str:
        """ new session
        """
        x = self._db
        try:
            u = x.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        x.update_user(u.id, session_id=session_id)
        return session_id
