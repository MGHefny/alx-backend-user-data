#!/usr/bin/env python3
""" filtering logs message """
from typing import List
import re
import logging
import os
import mysql.connector




def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """  """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message