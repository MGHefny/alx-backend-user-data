#!/usr/bin/env python3
""" filtering logs message """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """ filter datum message """
    for x in fields:
        message = re.sub(f'{x}=.*?{separator}',
                         f'{x}={redaction}{separator}', message)
    return message
