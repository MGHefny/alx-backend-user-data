#!/usr/bin/env python3
""" auth model"""
import bcrypt


def _hash_password(password: str) -> str:
    """ hash pass"""
    x = password.encode("utf-8")
    y = bcrypt.gensalt()
    encript_paw = bcrypt.hashpw(x, y)
    return encript_paw
