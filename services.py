import sqlite3

NAME_DATABASE = "PeriscoDatabase.db"

def get_db():
    """Connect the sqlite Database"""
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)

def setChild(childname):
    """Create the information of the child"""
    db = get_db()
    reqSQL = f"insert into Childs (childname) values ('{childname}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def getChilds():
    """read the childs"""
    db = get_db()
    reqSQL = f"select * from Childs"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def setActivity(activitydname):
    """Create one activity"""
    db = get_db()
    reqSQL = f"insert into Ativities (activityname) values ('{activityname}')  "
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