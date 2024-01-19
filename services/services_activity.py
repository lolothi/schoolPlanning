from services.services_sqlite_db import get_db
from services.services_usual_activity import checkExistingUsualactivitiesById, deleteUsualActivityByActivityId
from services.services_month_activities import check_existing_activity_in_month_activities

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
    if check_existing_activity_in_month_activities(activity_id) == False:
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
    reqSQL = """
    SELECT a.id, a.activity_name, a.activity_price, a.activity_time, a.activity_comment, CASE WHEN ma.activity_id IS NOT NULL THEN 1 ELSE 0 END used_in_month_activities
    FROM Activities a
    LEFT JOIN Month_activities ma ON a.id = ma.activity_id
    GROUP BY a.id, a.activity_name
    """
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def getActivityByName(activity_name):
    db = get_db()
    reqSQL = "select * from Activities WHERE activity_name = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity_name,))
    res = cur.fetchone()
    if res:
        db.close()
        return res
    db.close()

def checkNotExistingActivityByName(activity_name):
    reqSQL = "select * from Activities WHERE activity_name = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (activity_name,))
    res = cur.fetchone()
    if res:
        return False
    else:
        db.close()
        return True
