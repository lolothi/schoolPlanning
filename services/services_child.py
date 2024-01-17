from services.services_sqlite_db import get_db

def setChild(childname):
    db = get_db()
    reqSQL = f"insert into Childs (child_name) values ('{childname}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

def updateChild(id, newChildname):
    db = get_db()
    reqSQL = f"UPDATE Childs SET child_name ='{newChildname}' WHERE id = '{id}'  "
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