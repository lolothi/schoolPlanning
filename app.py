from flask import Flask, render_template, request, redirect
from datetime import datetime
import calendar
import services
from classes.JoursFeriesClass import JoursFeries, Jour
import functions_help


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

isInEditionMode = False
error = None
message = None

@app.route("/")
def index():
    today = datetime.today()
    print("calendar: ", calendar.monthcalendar(2023, 12))
    return render_template("home.html", today=today)

@app.route('/mode_edition', methods=["POST"])
def mode_edition():
    global isInEditionMode
    if request.method == "POST":
        if isInEditionMode is False:
            isInEditionMode=True
        else:
            isInEditionMode=False
    return redirect("/params")

@app.route('/child_delete/<int:item_id>', methods=["POST"])
def child_delete(item_id):
    if request.method == "POST":
        services.deleteChild(item_id)   
    return redirect("/params")

@app.route('/child_update/<int:item_id>', methods=["POST", "GET"])
def child_update(item_id):
    new_child_name = request.form.get("new_child_name")
    if request.method == "POST":
        services.updateChild(item_id, new_child_name)
    return redirect("/params")

@app.route('/child_create', methods=["POST"])
def child_create():
    global error
    global message

    child_name = request.form.get("child_name")

    if request.method == "POST":
        if child_name:
            try:
                services.setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"
    return redirect("/params")

@app.route('/activity_delete/<int:item_id>', methods=["POST"])
def activity_delete(item_id):
    if request.method == "POST":
        services.deleteActivity(item_id)   
    return redirect("/params")

@app.route('/activity_update/<int:item_id>', methods=["POST", "GET"])
def activity_update(item_id):
    new_activity = {
        'name' : request.form.get("new_activity_name"),
        'time' : request.form.get("new_activity_time"),
        'price' : request.form.get("new_activity_price"),
        'comment' : str(request.form.get("new_activity_comment"))
    }
    if request.method == "POST":
        services.updateActivity(item_id, new_activity)
    return redirect("/params")

@app.route('/activity_create', methods=["POST"])
def activity_create():
    global error
    global message
    
    activity = {
        'name' : request.form.get("activity_name"),
        'time' : request.form.get("activity_time"),
        'price' : request.form.get("activity_price"),
        'comment' : request.form.get("activity_comment")
    }

    if request.method == "POST":
        if activity['name']:
            try:
                if services.checkNotExistingActivityByName(activity['name']):
                    services.setActivity(activity)
                    message = "Activité créé"
                else:
                    error = "Nom déjà existant"
            except:
                error = "Erreur dans la création"

    return redirect("/params")

@app.route('/usual_activity_delete/<int:item_id>', methods=["POST"])
def usual_activity_delete(item_id):
    activity_name = request.form.get("usual_activity_name")
    if request.method == "POST":
        services.deleteUsualActivityByActivityName(item_id, activity_name)   
    return redirect("/params")

@app.route('/usual_activity_create', methods=["POST"])
def usual_activity_create():
    global error
    global message

    usual_activity = {
        'day' : request.form.get("activity_day"),
        'activity' : request.form.get("usual_activity")
    }

    if request.method == "POST":
        if usual_activity['day'] and usual_activity['activity']:
            try:
                if int(usual_activity['day']) > 0 and int(usual_activity['activity']) > 0:
                    services.setUsualActivity(usual_activity)
                    message = "Activité créé"
            except:
                error = "Erreur dans la création"

    return redirect("/params")

@app.route("/params", methods=["POST", "GET"])
def params():
    global error
    global message
    global isInEditionMode

    childsInDb = services.getChilds()
    activitiesInDb = services.getActivities()
    if services.getUsualActivities():
        usual_activities_in_DB_day_group = services.getListOfUsualActivitiesGroupByDay()
    else:
        usual_activities_in_DB_day_group = []

    JoursFeriesAnneeEnCours = JoursFeries()

    return render_template(
        "params.html",
        message=message,
        error=error,
        childsInDb=childsInDb,
        activitiesInDb=activitiesInDb,
        JoursFeriesAnneeEnCours=JoursFeriesAnneeEnCours.dumps(),
        usual_activities_in_DB=usual_activities_in_DB_day_group,
        Jour=Jour,
        stringToNumber=functions_help.stringToNumber,
        isInEditionMode=isInEditionMode   )


if __name__ == "__main__":
    app.run(debug=True)
