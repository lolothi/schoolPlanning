import sqlite3
import json

NAME_DATABASE = "PeriscoDatabase.db"

def get_db():
    """Connect the sqlite Database"""
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)

# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()
