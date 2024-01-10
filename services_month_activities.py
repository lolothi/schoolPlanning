from datetime import date
from services_sqlite_db import get_db

def set_new_month(year, month, payed = False):
    db = get_db()
    reqSQL = "INSERT INTO School_months (year, month, payed) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (year, month, payed,))
    db.commit()
    db.close()
    return cur.lastrowid
    

def get_months():
    db = get_db()
    reqSQL = "SELECT * from School_months"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        return res
    db.close()

def check_existing_month(year, month):
    reqSQL = f"SELECT * from School_months WHERE year = ? and month = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (year, month,))
    res = cur.fetchone()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False
    
# --- Month activities ---
def set_month_activities(date:date, activity_id, child_id, School_months_id, web_validated=0):
    print('set_month_activities',date, activity_id, child_id, School_months_id, web_validated)
    db = get_db()
    reqSQL = "INSERT INTO Month_activities (date, activity_id, child_id, school_months_id, web_validated) VALUES (?, ?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (date, activity_id, child_id, School_months_id, web_validated,))
    db.commit()
    db.close()