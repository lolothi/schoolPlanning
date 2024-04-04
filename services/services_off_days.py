from datetime import date, datetime
# import datetime
import calendar
from services.services_sqlite_db import get_db
from services.services_child import getChilds

def set_off_days(date:date, child_id:int, web_validated:bool=0, strike_canceled:bool=0, family_canceled:bool=0, school_canceled:bool=0 ):
    db = get_db()
    reqSQL = "INSERT INTO off_days (date, child_id, web_validated, strike_canceled, family_canceled, school_canceled) VALUES (?, ?, ?, ?, ?, ?)"
    if child_id == 0 :
        print('set_off_days_CHILD=0', child_id)
        for child in getChilds():
            cur = db.cursor()
            cur.execute(reqSQL, (date, child[0], web_validated, strike_canceled, family_canceled, school_canceled))
            db.commit()
    else : 
        cur = db.cursor()
        cur.execute(reqSQL, (date, child_id, web_validated, strike_canceled, family_canceled, school_canceled))
        db.commit()
    db.close()

# To check the canceled days when creating a new month with activities   
def get_off_days_by_month(year:int, month:int):
    off_days_by_month = []
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT date, child_id, school_canceled, family_canceled, strike_canceled FROM off_days WHERE date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        for off_day in res:
            # off_day_timestamp = int(datetime.datetime.timestamp(datetime.datetime.strptime(off_day[0], '%Y-%m-%d')))
            off_day_datetime = datetime.strptime(off_day[0], '%Y-%m-%d')
            off_day = {'date': off_day_datetime, 'child_id':off_day[1], 'school_canceled':off_day[2], 'family_canceled':off_day[3], 'strike_canceled':off_day[4]} 
            off_days_by_month.append(off_day)
        db.close()
        return off_days_by_month
    else:
        db.close()
        return []

def get_off_days_by_date_child(date: date, child_id:int):
    db = get_db()
    reqSQL = "SELECT school_canceled, family_canceled, strike_canceled FROM off_days WHERE date = ? and child_id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (date,child_id))
    res = cur.fetchone()
    if res:
        return res
    else:
        db.close()
        return []

def check_existing_off_day_by_date_child(date: date, child_id:int):
    reqSQL = "SELECT * from off_days WHERE date = ? and child_id = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (date,child_id))
    res = cur.fetchone()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False
    
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