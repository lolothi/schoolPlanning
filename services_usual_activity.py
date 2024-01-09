import json
from services_sqlite_db import get_db
from services_child import getChilds
# from services_activity import getActivityByName

def setUsualActivity(usual_activity):
    db = get_db()
    reqSQL = "INSERT INTO Usual_activities (day, activity_id, child_id) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (usual_activity['day'], usual_activity['activity'], usual_activity['child']))
    db.commit()
    db.close()

def setUsualActivityForAllChildren(usual_activity):
    reqSQL = "INSERT INTO Usual_activities (day, activity_id, child_id) VALUES (?, ?, ?)"
    db = get_db()
    for child in getChilds():
        cur = db.cursor()
        cur.execute(reqSQL, (usual_activity['day'], usual_activity['activity'], child[0]))
        db.commit()
    db.close()


def getUsualActivities():
    db = get_db()
    reqSQL = f"select * from Usual_activities ORDER BY day ASC"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def getListOfUsualActivitiesGroupByDay():
    db = get_db()
    reqSQL = f"SELECT u.day, '[' || GROUP_CONCAT(json_object('id', u.id, 'activity', a.activity_name, 'child', child_name)) || ']' AS activities_and_children from Usual_activities u INNER JOIN Activities a ON a.id = u.activity_id INNER JOIN Childs c ON c.id = u.child_id GROUP BY u.day"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        for i, (day, activities_json) in enumerate(res):
            activities_list = json.loads(activities_json)
            res[i] = (day, activities_list)
        return res
    db.close()

def checkExistingUsualactivitiesById(id):
    reqSQL = f"select id from Usual_activities WHERE id = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (id,))
    res = cur.fetchall()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False

def deleteUsualActivityByActivityName(usual_activity_id, activityname):
    db = get_db()
    reqSQL = "DELETE FROM Usual_activities WHERE id = ? AND activity_id IN (SELECT id FROM Activities WHERE activity_name = ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (usual_activity_id, activityname))
    db.commit()
    db.close()

def deleteUsualActivityByActivityId(activity_id):
    db = get_db()
    reqSQL = "DELETE FROM Usual_activities WHERE activity_id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (activity_id,))
    db.commit()
    db.close()
