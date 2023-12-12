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

def updateChild(id, newChildname):
    """Create the information of the child"""
    db = get_db()
    reqSQL = f"UPDATE Childs SET childname ='{newChildname}' WHERE id = '{id}'  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def deleteChild(childId):
    db = get_db()
    reqSQL = f"DELETE FROM Childs WHERE id = '{childId}'  "
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


def setActivity(activityname, activityprice, activitytime="", activitycomment=""):
    """Create one activity"""
    db = get_db()
    reqSQL = f"insert into Activities (activityname, activityprice, activitytime, activitycomment) values ('{activityname}', '{activityprice}', '{activitytime}', '{activitycomment}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def getActivities():
    """read the activities"""
    db = get_db()
    reqSQL = f"select * from Activities"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()


def setUsualActivity(day, activity_id):
    """Create one usual activity"""
    db = get_db()
    reqSQL = f"insert into Usualactivities (day, activity_id) values ('{day}', '{activity_id}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def getUsualActivities():
    """read the usual activities"""
    db = get_db()
    reqSQL = f"select * from Usualactivities ORDER BY day ASC"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()


def getListOfUsualActivitiesGroupByDay():
    """read the usual activities"""
    db = get_db()
    reqSQL = f"SELECT day, GROUP_CONCAT(activity_id) AS activities_list from Usualactivities GROUP BY day"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()


# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()
