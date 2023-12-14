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
    reqSQL = "INSERT INTO Activities (activityname, activityprice, activitytime, activitycomment) VALUES (?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (activity['name'], activity['price'], activity['time'], activity['comment']))
    db.commit()
    db.close()

def updateActivity(id, activity):
    db = get_db()
    reqSQL = "UPDATE Activities SET activityname = ?, activityprice = ?, activitytime = ?, activitycomment = ? WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity['name'], activity['price'], activity['time'], activity['comment'], id))
    db.commit()
    db.close()

def deleteActivity(id):
    if checkExistingUsualactivitiesById(id):
        deleteUsualActivity(id)
    db = get_db()
    reqSQL = "DELETE FROM Activities WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (id,))
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

def checkNotExistingActivityByName(activity_name):
    reqSQL = f"select * from Activities WHERE activityname = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (activity_name,))
    res = cur.fetchone()
    if res:
        return False
    else:
        db.close()
        return True

def setUsualActivity(usual_activity):
    db = get_db()
    reqSQL = "INSERT INTO Usualactivities (day, activity_id) VALUES (?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (usual_activity['day'], usual_activity['activity']))
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

def deleteUsualActivity(id):
    db = get_db()
    reqSQL = "DELETE FROM Usualactivities WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (id,))
    db.commit()
    db.close()

def getListOfUsualActivitiesGroupByDay():
    db = get_db()
    reqSQL = f"SELECT Usualactivities.id, day, GROUP_CONCAT(activityname) AS activities_name_list from Usualactivities INNER JOIN Activities ON Activities.id = Usualactivities.activity_id GROUP BY day"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def checkExistingUsualactivitiesById(id):
    reqSQL = f"select id from Usualactivities WHERE id = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (id,))
    res = cur.fetchall()
    if res:
        return True
    else:
        db.close()
        return False

# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()
