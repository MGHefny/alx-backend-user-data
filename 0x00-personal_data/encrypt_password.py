#!/usr/bin/env python3
""" pass encr """
import bcrypt


def hash_password(password: str) -> bytes:
    """ re pass bytes """
    encrip = password.encode()
    h_h = bcrypt.hashpw(bcrypt.gensalt(), encrip)

    return h_h


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ prov pass """
    encrip = password.encode()
    return bcrypt.checkpw(encrip, hashed_password)
