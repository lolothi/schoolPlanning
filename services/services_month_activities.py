from datetime import date, datetime
import calendar
import json
from services.services_sqlite_db import get_db
from services.services_child import getChilds
from services.services_off_days import get_family_off_days_by_month, get_school_off_days_by_month
from functions_help import month_days

# --- school Month ---
def set_new_month(year, month, school_days=None):
    print('set_new_month', year, month, school_days)
    db = get_db()
    reqSQL = "INSERT INTO School_months (year, month, school_days) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (year, month, school_days,))
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
    reqSQL = "SELECT id, year, month, payed, school_days from School_months ORDER BY year, month ASC"
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
                "activities_count": len(get_activities_by_month(acitivity_in_month[1], acitivity_in_month[2])),
                "price_activities": get_activities_price_by_month(acitivity_in_month[1], acitivity_in_month[2]),
                "off_days": len(get_family_off_days_by_month(acitivity_in_month[1], acitivity_in_month[2])),
                "school_off_days": len(get_school_off_days_by_month(acitivity_in_month[1], acitivity_in_month[2])),
            }
            res_with_details.append(result_dict)
        return res_with_details
    db.close()

def check_existing_month(year, month):
    reqSQL = "SELECT * from School_months WHERE year = ? and month = ?"
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
def set_month_activity(date:date, activity_id:int, child_id:int, web_validated=0):
    print('--set_month_activity--: ', date, activity_id, child_id)
    db = get_db()
    reqSQL = "INSERT INTO Month_activities (date, activity_id, child_id) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (date, activity_id, child_id))
    db.commit()
    db.close()

def set_month_activity_for_all_children(date:date, activity_id:int, web_validated=0):   
    reqSQL = "INSERT INTO Month_activities (date, activity_id, child_id, web_validated) VALUES (?, ?, ?, ?, ?)"
    db = get_db()
    for child in getChilds():
        cur = db.cursor()
        cur.execute(reqSQL, (date, activity_id, child[0], web_validated,))
        db.commit()
    db.close()
    
def get_activities_by_month(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT id, date, activity_id, child_id, web_validated, school_canceled, family_canceled, strike_canceled, comment_id from Month_activities WHERE date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    # activities_dates = { day[1]: day for day in res}
    # print('get_activities_by_month',f"{year}-{month}-01", f"{year}-{month}-{last_day}", res)
    if res:
        db.close()
        return res
    else:
        db.close()
        return []
    
def get_activities_by_month_group_by_day(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = """SELECT date, '[' || GROUP_CONCAT(json_object('id', ma.id, 'name', a.activity_name, 'price', a.activity_price, 'child', child_name, 'web_validated', web_validated,'school_canceled',school_canceled, 'family_canceled', family_canceled,'strike_canceled', strike_canceled)) || ']' AS activities_and_children from Month_activities ma INNER JOIN Activities a ON a.id = ma.activity_id INNER JOIN Childs c ON c.id = ma.child_id WHERE date BETWEEN ? AND ? GROUP BY ma.date """
    # reqSQL = """SELECT DATE(ma.date) AS date, '[' || GROUP_CONCAT(json_object('id', ma.id, 'name', a.activity_name)) || ']' AS activities_and_children from Month_activities ma LEFT JOIN Activities a ON a.id = ma.activity_id INNER JOIN Childs c ON c.id = ma.child_id WHERE date BETWEEN ? AND ? GROUP BY DATE(ma.date) """
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    # print('--activities_dict_RES: ', res)
    if res:
        db.close()
        activities_dict = { 
            datetime.strptime(day, '%Y-%m-%d').date() : json.loads(activities_json) for i, (day, activities_json) in enumerate(res)}
        # print('--activities_dict: ', activities_dict)
        return activities_dict
    else:
        db.close()
        return {}

def get_price_by_month(year, month):
    db = get_db()
    reqSQL = "SELECT SUM(activity_price) FROM Month_activities WHERE date BETWEEN ? AND ? GROUP BY date"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month}-01", f"{year}-{month+1}-01"))
    res = cur.fetchall()
    if res:
        db.close()
        return res[0][0]
    else:
        db.close()
        return 0 
      

def get_activities_price_by_month(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT SUM(a.activity_price) FROM Month_activities ma INNER JOIN Activities a ON ma.activity_id = a.id WHERE date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return res[0][0]
    else:
        db.close()
        return 0  

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
    
def check_existing_activity_in_month_activities(activity_id):
    reqSQL = "SELECT * from Month_activities WHERE activity_id = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQL, (activity_id,))
    res = cur.fetchone()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False