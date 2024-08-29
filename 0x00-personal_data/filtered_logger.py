#!/usr/bin/env python3
""" filtering logs message """
from typing import List
import re
import logging
import os
import mysql.connector.connection


PII_FIELDS = ("name", "email", "phone", "ssn", "u_pass")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter datum message """
    for x in fields:
        message = re.sub(f'{x}=.*?{separator}',
                         f'{x}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ handel logger output """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    in_format = logging.StreamHandler()
    style = RedactingFormatter(list(PII_FIELDS))
    in_format.setFormatter(style)
    logger.addHandler(in_format)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ SQL DB """
    u_name_db = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    u_pass = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    local_host_db = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    name_db = os.getenv('PERSONAL_DATA_DB_NAME', "")

    cnn = mysql.connector.connect(
        user=u_name_db,
        password=u_pass,
        host=local_host_db,
        database=name_db
        )
    return cnn


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ main init function """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format output filter datum """
        alart = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            alart, self.SEPARATOR)


def main():
    """ the main function """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    f_name = cursor.column_names
    for z in cursor:
        alart = "".join("{}={}; ".format(a, b) for a, b in zip(f_name, z))
        logger.info(alart.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
