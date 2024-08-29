#!/usr/bin/env python3
"""
Main file
"""

import mysql.connector
from filtered_logger import get_db

def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
