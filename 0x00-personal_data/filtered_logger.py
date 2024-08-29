#!/usr/bin/env python3
""" filtering logs message """
from typing import List
import re
import logging
import os
import mysql.connector



def filter_datum(fields, redaction, message, separator):
    pattern = re.compile(f'({"|".join(map(re.escape, fields))}){re.escape(separator)}([^ {separator}]*)')
    return pattern.sub(lambda m: f'{m.group(1)}{separator}{redaction}', message)
