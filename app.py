from flask import Flask, render_template, request
from datetime import datetime
import calendar
import services

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
def index():
    today = datetime.today()
    print('calendar: ',calendar.monthcalendar(2023,12) )
    return render_template('home.html', today=today)

@app.route('/params', methods=["POST", "GET"])
def params():
    error = None
    message = None

    """Child creation"""
    child_name = request.form.get("child_name")
    childsInDb = services.getChilds()

    """Activity creation"""
    activity_name = request.form.get("activity_name")
    activity_time = request.form.get("activity_time")
    activity_price = request.form.get("activity_price")
    activity_comment = request.form.get("activity_comment")

    activitiesInDb = services.getActivities()

    if request.method == "POST":
        if child_name:
            try:
                services.setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"

        if activity_name:
            try:
                services.setActivity(activity_name, activity_price, activity_time, activity_comment)
                message = "Activitée créé"
            except:
                error = "Erreur dans la création"

    return render_template("params.html", message=message, error=error, childsInDb=childsInDb, activitiesInDb=activitiesInDb, child_name=child_name, activity_name=activity_name, activity_time=activity_time, activity_price=activity_price, activity_comment=activity_comment)

if __name__ == '__main__':
    app.run(debug=True)