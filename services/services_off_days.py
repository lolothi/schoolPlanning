from datetime import date
from services.services_sqlite_db import get_db
from services.services_child import getChilds

def set_off_days(date:date, child_id:int, web_validated:bool=0, school_canceled:bool=0):
    db = get_db()
    reqSQL = "INSERT INTO off_days (date, child_id, web_validated, school_canceled) VALUES (?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (date, child_id, web_validated, school_canceled))
    db.commit()
    db.close()

def set_off_days_for_all_children(date:date, web_validated:bool=0, school_canceled:bool=0):
    reqSQL = "INSERT INTO off_days (date, child_id, web_validated, school_canceled) VALUES (?, ?, ?, ?)"
    db = get_db()
    for child in getChilds():
        cur = db.cursor()
        cur.execute(reqSQL, (date, child[0], web_validated, school_canceled))
        db.commit()
    db.close()