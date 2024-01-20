from services.services_sqlite_db import get_db


def setChild(child_name):
    db = get_db()
    reqSQL = f"insert into Childs (child_name) values ('{child_name}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def updateChild(id, new_child_name):
    db = get_db()
    reqSQL = f"UPDATE Childs SET child_name ='{new_child_name}' WHERE id = '{id}'  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def deleteChild(child_id):
    if check_existing_child_in_month_activities(child_id) == False:
        db = get_db()
        reqSQL = f"DELETE FROM Childs WHERE id = '{child_id}'  "
        cur = db.cursor()
        cur.execute(reqSQL)
        db.commit()
        db.close()


def getChilds():
    db = get_db()
    reqSQL = """
    SELECT c.id, c.child_name, CASE WHEN ma.child_id IS NOT NULL THEN 1 ELSE 0 END used_in_month_activities 
    FROM Childs c 
    LEFT JOIN Month_activities ma ON c.id = ma.child_id
    GROUP BY c.id, c.child_name"""
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def check_existing_child_in_month_activities(child_id):
    reqSQL = "SELECT * from Month_activities WHERE child_id = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (child_id,))
    res = cur.fetchone()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False
