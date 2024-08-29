#!/usr/bin/env python3
""" filtering logs message """
from typing import List
import re


def filter_datum(fields, redaction, message, separator):
    """ filter datum message """
    for x in fields:
        message = re.sub(f'{x}=.*?{separator}',
                         f'{x}={redaction}{separator}', message)
    return message
