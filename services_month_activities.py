from services_sqlite_db import get_db

def set_new_month(year, month, payed = False):
    db = get_db()
    reqSQL = "INSERT INTO School_months (year, month, payed) VALUES (?, ?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (year, month, payed,))
    db.commit()
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
