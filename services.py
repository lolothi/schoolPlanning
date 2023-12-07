import sqlite3

NAME_DATABASE = "PeriscoDatabase.db"

def get_db():
    """Connect the sqlite Database"""
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)

def setInfoChild(childname):
    """Create the information of the connected user"""
    db = get_db()
    reqSQL = f"insert into Childs (username) values ('{childname}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()