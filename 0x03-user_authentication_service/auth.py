#!/usr/bin/env python3
""" auth model
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ finde user in sec
        """
        x = self._db
        if session_id is None:
            return None
        try:
            u = x.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return u

    def destroy_session(self, user_id: int) -> None:
        """ end sec
        """
        x = self._db
        try:
            u = x.find_user_by(id=user_id)
        except NoResultFound:
            return None
        x.update_user(u.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ res pass
        """
        x = self._db
        try:
            u = x.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        x.update_user(u.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ new pass
        """
        x = self._db
        if reset_token is None or password is None:
            return None
        try:
            u = x.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        x.update_user(u.id, hashed_password=hashed_password, reset_token=None)
