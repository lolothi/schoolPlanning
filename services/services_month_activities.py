from datetime import date, datetime
import calendar
import json
from services.services_sqlite_db import get_db
from services.services_child import getChilds
from functions_help import calculate_real_activities_in_month

# --- school Month ---
def set_new_month(year, month, school_days=None):
    db = get_db()
    reqSQL = "INSERT INTO School_months (year, month, school_days) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(
        reqSQL,
        (
            year,
            month,
            school_days,
        ),
    )
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

def delete_month_and_activities(month_id:int, year, month):  
    reqSQLdelMonth = "DELETE from School_months WHERE id = ?"

    db = get_db()
    cur = db.cursor()
    cur.execute(reqSQLdelMonth, (month_id, ))
    db.commit()
    delete_activities(year, month)

def delete_activities(year, month):  
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQLcheck = "SELECT * FROM Month_activities WHERE date BETWEEN ? AND ?"
    reqSQLdelActivities = "DELETE FROM Month_activities WHERE date BETWEEN ? AND ?"
    
    db = get_db()
    cur = db.cursor()

    cur.execute(reqSQLcheck, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    db.commit()
    
    if res:
        cur.execute(reqSQLdelActivities, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
        db.commit()
    db.close()

# Important get_months_with_details from School_months table because of empty month (without activities)
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
            (
                total_price,
                total_activities,
                total_school_canceled,
                total_family_canceled,
                total_strike_canceled,
            ) = get_real_activities_price_and_real_counted_activities_by_month(
                acitivity_in_month[1], acitivity_in_month[2]
            )
            result_dict = {
                "month_id": acitivity_in_month[0],
                "year": acitivity_in_month[1],
                "month": acitivity_in_month[2],
                "school_days": acitivity_in_month[4],
                "activities_count": total_activities,
                "price_activities": total_price,
                "off_days": total_family_canceled,
                "school_off_days": total_school_canceled,
                "strike_days": total_strike_canceled,
            }
            res_with_details.append(result_dict)
        return res_with_details
    db.close()


def check_existing_month(year, month):
    reqSQL = "SELECT * from School_months WHERE year = ? and month = ?"
    db = get_db()
    cur = db.cursor()
    cur.execute(
        reqSQL,
        (
            year,
            month,
        ),
    )
    res = cur.fetchone()
    if res:
        db.close()
        return res[0]
    else:
        db.close()
        return None


# --- Month activities ---
def set_month_activity(date: date, activity_id: int, child_id: int, web_validated=0):
    print("--set_month_activity--: ", date, activity_id, child_id)
    db = get_db()
    reqSQL = (
        "INSERT INTO Month_activities (date, activity_id, child_id) VALUES (?, ?, ?)"
    )
    cur = db.cursor()
    cur.execute(reqSQL, (date, activity_id, child_id))
    db.commit()
    db.close()


def set_month_activity_for_all_children(date: date, activity_id: int, web_validated=0):
    reqSQL = "INSERT INTO Month_activities (date, activity_id, child_id, web_validated) VALUES (?, ?, ?, ?, ?)"
    db = get_db()
    for child in getChilds():
        cur = db.cursor()
        cur.execute(
            reqSQL,
            (
                date,
                activity_id,
                child[0],
                web_validated,
            ),
        )
        db.commit()
    db.close()


def get_activities_by_month_day(year, month, month_day):
    db = get_db()
    month_str = str(month).zfill(2)
    month_day_str = str(month_day).zfill(2)
    reqSQL = """SELECT ma.id, a.activity_name, c.child_name, 
    ma.web_validated, ma.school_canceled, family_canceled, strike_canceled, comment_id
    FROM Month_activities ma 
    INNER JOIN Activities a ON ma.activity_id = a.id 
    INNER JOIN Childs c ON c.id = ma.child_id 
    WHERE date = ?"""
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-{month_day_str}",))
    res = cur.fetchall()
    print('##get_activities_by_month_day:' ,f"{year}-{month_str}-{month_day_str}")
    if res:
        db.close()
        activities_list = []
        for row in res:
            activity_dict = {
                'id': row[0],
                'activity_name': row[1],
                'child_name': row[2],
                'web_validated': row[3],
                'school_canceled': row[4],
                'family_canceled': row[5],
                'strike_canceled': row[6],
                'comment_id': row[7]
            }
            activities_list.append(activity_dict)
        return activities_list
    else:
        db.close()
        return []

def update_month_activity(id, month_activity):
    db = get_db()
    reqSQL = "UPDATE Month_activities SET web_validated = ?, school_canceled = ?, family_canceled = ?, strike_canceled = ? , comment_id = ? WHERE id = ?"
    cur = db.cursor()
    cur.execute(reqSQL, (month_activity['web_validated'], month_activity['school_canceled'], month_activity['family_canceled'], month_activity['strike_canceled'], month_activity['comment_id'], id))
    db.commit()
    db.close()

def get_activities_by_month_group_by_day(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = """SELECT date, '[' || GROUP_CONCAT(json_object('id', ma.id, 'name', a.activity_name, 'price', a.activity_price, 'child', child_name, 'web_validated', web_validated,'school_canceled',school_canceled, 'family_canceled', family_canceled,'strike_canceled', strike_canceled)) || ']' AS activities_and_children from Month_activities ma INNER JOIN Activities a ON a.id = ma.activity_id INNER JOIN Childs c ON c.id = ma.child_id WHERE date BETWEEN ? AND ? GROUP BY ma.date """
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        activities_dict = {
            # dictionary with activities listed by day
            datetime.strptime(day, "%Y-%m-%d").date(): json.loads(activities_json)
            for i, (day, activities_json) in enumerate(res)
        }
        return activities_dict
    else:
        db.close()
        return {}


def get_real_activities_price_and_real_counted_activities_by_month(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = """SELECT 
    IFNULL(SUM(CASE WHEN ma.school_canceled = 0 AND ma.family_canceled = 0 AND ma.strike_canceled = 0 THEN a.activity_price ELSE 0 END), 0) AS total_price, 
    IFNULL(SUM(CASE WHEN ma.school_canceled = 0 AND ma.family_canceled = 0 AND ma.strike_canceled = 0 THEN 1 ELSE 0 END), 0) AS total_activities, 
    IFNULL(SUM(ma.school_canceled),0) AS total_school_canceled, 
    IFNULL(SUM(ma.family_canceled),0) AS total_family_canceled, 
    IFNULL(SUM(ma.strike_canceled),0) AS total_strike_canceled
    FROM Month_activities ma 
    INNER JOIN Activities a ON ma.activity_id = a.id
    WHERE date BETWEEN ? AND ?"""
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return res[0]
    else:
        db.close()
        return []


def get_activities_price_by_month_group_by_child_activity(year, month):
    res_with_details = []
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = """SELECT c.child_name, a.activity_name, a.activity_price, 
    SUM(a.activity_price) AS total_price, 
    COUNT(*) AS total_activities, 
    SUM(ma.school_canceled) AS total_school_canceled, 
    SUM(ma.family_canceled) AS total_family_canceled, 
    SUM(ma.strike_canceled) AS total_strike_canceled
    FROM Month_activities ma 
    INNER JOIN Activities a ON ma.activity_id = a.id 
    INNER JOIN Childs c ON c.id = ma.child_id 
    WHERE date BETWEEN ? AND ? GROUP by ma.child_id, a.activity_name"""
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        for child_activity in res:
            # for canceled activities substraction
            real_activities = calculate_real_activities_in_month(
                child_activity[4],
                child_activity[2],
                child_activity[3],
                child_activity[5],
                child_activity[6],
                child_activity[7],
            )
            result_dict = {
                "child_name": child_activity[0],
                "activity_name": child_activity[1],
                "activity_price": child_activity[2],
                "total_price": child_activity[3],
                "real_total_price": real_activities["real_total_price"],
                "total_activities": child_activity[4],
                "real_total_activities": real_activities["real_total_activities"],
                "canceled_activities": child_activity[5]
                + child_activity[6]
                + child_activity[7],
            }
            res_with_details.append(result_dict)
        db.close()
        return res_with_details
    else:
        db.close()
        return []



def check_existing_activities_in_month(year, month):
    db = get_db()
    month_str = str(month).zfill(2)
    last_day = calendar.monthrange(year, month)[1]
    reqSQL = "SELECT * from Month_activities date BETWEEN ? AND ?"
    cur = db.cursor()
    cur.execute(reqSQL, (f"{year}-{month_str}-01", f"{year}-{month_str}-{last_day}"))
    res = cur.fetchall()
    if res:
        db.close()
        return True
    else:
        db.close()
        return False

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


# Month Activities : DAYS OFF
def set_day_off_on_activity(
    date: date,
    child_id: int,
    web_validated: bool = 0,
    strike_canceled: bool = 0,
    family_canceled: bool = 0,
    school_canceled: bool = 0,
):
    db = get_db()
    reqSQL = ""
    if child_id == 0:
        if strike_canceled == 1:
            reqSQL = "UPDATE Month_activities SET strike_canceled = 1 WHERE date = ?"
        elif family_canceled == 1:
            reqSQL = "UPDATE Month_activities SET family_canceled = 1 WHERE date = ?"
        elif school_canceled == 1:
            reqSQL = "UPDATE Month_activities SET school_canceled = 1 WHERE date = ?"
        cur = db.cursor()
        cur.execute(reqSQL, (date,))
    else:
        if strike_canceled == 1:
            reqSQL = "UPDATE Month_activities SET strike_canceled = 1 WHERE date = ? and child_id = ?"
        elif family_canceled == 1:
            reqSQL = "UPDATE Month_activities SET family_canceled = 1 WHERE date = ? and child_id = ?"
        elif school_canceled == 1:
            reqSQL = "UPDATE Month_activities SET school_canceled = 1 WHERE date = ? and child_id = ?"
        cur = db.cursor()
        cur.execute(reqSQL, (date, child_id))
    db.commit()
    db.close()
