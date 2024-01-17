from datetime import date
from services.services_sqlite_db import get_db
from functions_help import month_holidays_closed

# --- school Month ---
def set_new_month(year, month, school_days, payed = False):
    db = get_db()
    reqSQL = "INSERT INTO School_months (year, month, payed, school_days) VALUES (?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (year, month, payed, school_days,))
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

def get_months_with_details():
    res_with_details = []
    db = get_db()
    reqSQL = "SELECT * from School_months"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchall()
    if res:
        db.close()
        for acitivity_in_month in res:
            result_dict = {
                "month_id": acitivity_in_month[0],
                "year": acitivity_in_month[1],
                "month": acitivity_in_month[2],
                "school_days": acitivity_in_month[4],
                "activities_count": len(get_activities_by_month_id(acitivity_in_month[0])),
                "price_activities": get_price_by_month_id(acitivity_in_month[0]),
                "off_days": len(month_holidays_closed(acitivity_in_month[1], acitivity_in_month[2])), #a finaliser,
                "school_off_days": acitivity_in_month[0], #a finaliser,
            }
            res_with_details.append(result_dict)
        return res_with_details
    db.close()

def check_existing_month(year, month):
    reqSQL = f"SELECT * from School_months WHERE year = ? and month = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (year, month,))
    res = cur.fetchone()
    if res:
        db.close()
        return res[0]
    else:
        db.close()
        return None

# --- Month activities ---
def set_month_activities(date:date, activity_id:int, child_id:int, School_months_id:int, web_validated=0):
    db = get_db()
    reqSQL = "INSERT INTO Month_activities (date, activity_id, child_id, school_months_id, web_validated) VALUES (?, ?, ?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (date, activity_id, child_id, School_months_id, web_validated,))
    db.commit()
    db.close()

def get_activities_by_month_id(school_months_id:int):
    db = get_db()
    reqSQL = "SELECT * from Month_activities WHERE school_months_id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (school_months_id,))
    res = cur.fetchall()
    if res:
        db.close()
        return res[0]
    else:
        db.close()
        return []

def get_price_by_month_id(school_months_id):
    db = get_db()
    reqSQL = "SELECT SUM(a.activity_price) FROM Month_activities ma INNER JOIN Activities a ON ma.activity_id = a.id WHERE ma.school_months_id = ? group by ma.school_months_id "
    cur = db.cursor()
    cur.execute(reqSQL, (school_months_id,))
    res = cur.fetchall()
    if res:
        db.close()
        return res[0][0]
    else:
        db.close()
        return 0    

