from datetime import date
from services.services_sqlite_db import get_db

def set_off_days(date:date, child_id:int):
    db = get_db()
    reqSQL = "INSERT INTO off_days (date, child_id) VALUES (?, ?)"
    cur = db.cursor()
    cur.execute(reqSQL, (date, child_id))
    db.commit()
    db.close()