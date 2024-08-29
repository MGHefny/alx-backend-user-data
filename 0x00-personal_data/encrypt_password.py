#!/usr/bin/env python3
""" pass encr """
import bcrypt


def hash_password(password: str) -> bytes:
    """ re pass bytes """
    encrip = password.encode('utf-8')
    h_h = bcrypt.hashpw(bcrypt.gensalt(), encrip)

    return h_h


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ prov pass """
    encrip = password.encode('utf-8')
    return bcrypt.checkpw(encrip, hashed_password)
