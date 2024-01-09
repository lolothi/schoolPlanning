from services_sqlite_db import get_db
from services_usual_activity import checkExistingUsualactivitiesById, deleteUsualActivityByActivityId

def setActivity(activity):
    if activity['time'] == "":
        activity['time'] = 0
    if activity['comment'] == "":
        activity['comment']= '-'

    db = get_db()
    reqSQL = "INSERT INTO Activities (activity_name, activity_price, activity_time, activity_comment) VALUES (?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (activity['name'], activity['price'], activity['time'], activity['comment']))
    db.commit()
    db.close()

def updateActivity(id, activity):
    db = get_db()
    reqSQL = "UPDATE Activities SET activity_name = ?, activity_price = ?, activity_time = ?, activity_comment = ? WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity['name'], activity['price'], activity['time'], activity['comment'], id))
    db.commit()
    db.close()

def deleteActivity(activity_id):
    if checkExistingUsualactivitiesById(activity_id):
        deleteUsualActivityByActivityId(activity_id)
    db = get_db()
    reqSQL = "DELETE FROM Activities WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity_id,))
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

def getActivityByName(activity_name):
    db = get_db()
    reqSQL = f"select * from Activities WHERE activity_name = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity_name,))
    res = cur.fetchone()
    if res:
        db.close()
        return res
    db.close()

def checkNotExistingActivityByName(activity_name):
    reqSQL = f"select * from Activities WHERE activity_name = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (activity_name,))
    res = cur.fetchone()
    if res:
        return False
    else:
        db.close()
        return True
