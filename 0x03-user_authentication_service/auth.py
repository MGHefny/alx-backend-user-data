#!/usr/bin/env python3
""" auth model"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> str:
    """ hash pass"""
    x = password.encode("utf-8")
    y = bcrypt.gensalt()
    encript_paw = bcrypt.hashpw(x, y)
    return encript_paw


class Auth:
    """ auth cls
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ login user """
        x = self._db
        try:
            u = x.find_user_by(email=email)
        except NoResultFound:
            hash_paw = _hash_password(password)
            u = x.add_user(email, hash_paw)
            return u
        else:
            raise ValueError(f'User {email} already exists')
