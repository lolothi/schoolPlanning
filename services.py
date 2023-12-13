import sqlite3

NAME_DATABASE = "PeriscoDatabase.db"


def get_db():
    """Connect the sqlite Database"""
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)


def setChild(childname):
    db = get_db()
    reqSQL = f"insert into Childs (childname) values ('{childname}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def updateChild(id, newChildname):
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

def setActivity(activity):
    if activity['time'] == "":
        activity['time'] = 0
    if activity['comment'] == "":
        activity['comment']= '-'

    db = get_db()
    reqSQL = f"insert into Activities (activityname, activityprice, activitytime, activitycomment) values ('{activity['name']}', '{activity['price']}', '{activity['time']}', '{activity['comment']}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def updateActivity(id, activity):
    db = get_db()
    reqSQL = f"UPDATE Activities SET activityname = '{activity['name']}', activityprice = '{activity['price']}', activitytime = '{activity['time']}', activitycomment = '{activity['comment']}' WHERE id = '{id}'  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def deleteActivity(id):
    db = get_db()
    reqSQL = f"DELETE FROM Activities WHERE id = '{id}'  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def getActivities():
    db = get_db()
    reqSQL = f"select * from Activities"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()


def setUsualActivity(usual_activity):
    db = get_db()
    reqSQL = f"insert into Usualactivities (day, activity_id) values ('{usual_activity['day']}', '{usual_activity['activity']}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def getUsualActivities():
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
