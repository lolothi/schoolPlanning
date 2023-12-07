from flask import Flask, render_template, request
from datetime import datetime
import calendar

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
def index():
    today = datetime.today()
    print('calendar: ',calendar.monthcalendar(2023,12) )
    return render_template('mois.html', today=today)

@app.route('/params')
def params():
    """Child creation"""
    error = None
    message = None
    child_name = request.form.get("child_name")
    return render_template("params.html", message=message, error=error, child_name=child_name)
