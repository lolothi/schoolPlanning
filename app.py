from flask import Flask, render_template, request, redirect
from datetime import datetime
import calendar
import services
from classes.JoursFeriesClass import JoursFeries, Jour
import functions_help


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

isInEditionMode = False

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

@app.route('/usual_activity_delete/<int:item_id>', methods=["POST"])
def usual_activity_delete(item_id):
    if request.method == "POST":
        # services.deleteUsualActivity(item_id)   
        print('---DELETE')
    return redirect("/params")

@app.route("/params", methods=["POST", "GET"])
def params():
    error = None
    message = None
    global isInEditionMode

    """Child creation"""
    child_name = request.form.get("child_name")
    childsInDb = services.getChilds()

    """Activity creation"""
    activity = {
        'name' : request.form.get("activity_name"),
        'time' : request.form.get("activity_time"),
        'price' : request.form.get("activity_price"),
        'comment' : request.form.get("activity_comment")
    }
    
    activitiesInDb = services.getActivities()

    """Usual Activities creation"""
    usual_activity = {
        'day' : request.form.get("activity_day"),
        'activity' : request.form.get("usual_activity")
    }
    

    # usual_activities_in_DB = services.getUsualActivities()
    if services.getUsualActivities():
        usual_activities_in_DB_day_group = services.getListOfUsualActivitiesGroupByDay()
    else:
        usual_activities_in_DB_day_group = []

    if request.method == "POST":
        if child_name:
            try:
                services.setChild(child_name)

                message = "Enfant créé"
            except:
                error = "Erreur dans la création"

        if activity['name']:
            try:
                if services.checkNotExistingActivityByName(activity['name']):
                    services.setActivity(activity)
                    message = "Activité créé"
                else:
                    error = "Nom déjà existant"
            except:
                error = "Erreur dans la création"

        if usual_activity['day'] and usual_activity['activity']:
            try:
                if int(usual_activity['day']) > 0 and int(usual_activity['activity']) > 0:
                    services.setUsualActivity(usual_activity)
                    message = "Activité créé"
            except:
                error = "Erreur dans la création"

    """jours fériés"""
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
