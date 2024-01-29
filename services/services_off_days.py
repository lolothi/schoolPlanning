from datetime import date
import calendar
from services.services_sqlite_db import get_db
from services.services_child import getChilds

def set_off_days(date:date, child_id:int, web_validated:bool=0, strike_canceled:bool=0, family_canceled:bool=0, school_canceled:bool=0 ):
    db = get_db()
    reqSQL = "INSERT INTO off_days (date, child_id, web_validated, strike_canceled, family_canceled, school_canceled) VALUES (?, ?, ?, ?, ?, ?)"
    print('set_off_days',date, child_id, web_validated, strike_canceled, family_canceled, school_canceled )
    if child_id == 0 :
        print('set_off_days_CHILD=0', child_id)
        for child in getChilds():
            cur = db.cursor()
            cur.execute(reqSQL, (date, child[0], web_validated, strike_canceled, family_canceled, school_canceled))
            db.commit()
    else : 
        print('set_off_days_CHILD=??', child_id)
        cur = db.cursor()
        cur.execute(reqSQL, (date, child_id, web_validated, strike_canceled, family_canceled, school_canceled))
        db.commit()
    db.close()

def get_family_off_days_by_month(year:int, month:int):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT distinct date, family_canceled FROM off_days WHERE family_canceled = 1 and date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return res
    else:
        db.close()
        return []
    
def get_strikes_days_by_month(year:int, month:int):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT distinct date, strike_canceled FROM off_days WHERE strike_canceled = 1 and date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return res
    else:
        db.close()
        return []

def get_school_canceled_by_month(year:int, month:int):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT distinct date, school_canceled FROM off_days WHERE school_canceled = 1 and date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return res
    else:
        db.close()
        return []