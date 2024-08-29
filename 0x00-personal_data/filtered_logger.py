#!/usr/bin/env python3
""" filter datum return log message """
import re


def filter_datum(fields, redaction, message, separator):
    """ log message """
    for x in fields:
        message = re.sub(x+'=.*?'+separator,
                         x+'='+redaction+separator, message)
    return message
