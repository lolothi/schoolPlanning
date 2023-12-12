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
    print('EDITIONMODEchanges')
    global isInEditionMode
    if request.method == "POST":
        if isInEditionMode is False:
            isInEditionMode=True
        else:
            isInEditionMode=False
    return redirect("/params")

@app.route('/params_delete/<int:item_id>', methods=["POST"])
def params_delete(item_id):
    if request.method == "POST":
        services.deleteChild(item_id)   
    return redirect("/params")

@app.route('/params_update/<int:item_id>', methods=["POST", "GET"])
def params_update(item_id):
    new_child_name = request.form.get("new_child_name")
    if request.method == "POST":
        services.updateChild(item_id, new_child_name)
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
    activity_name = request.form.get("activity_name")
    activity_time = request.form.get("activity_time")
    activity_price = request.form.get("activity_price")
    activity_comment = request.form.get("activity_comment")

    activitiesInDb = services.getActivities()

    """Usual Activities creation"""
    activity_day = request.form.get("activity_day")
    usual_activity = request.form.get("usual_activity")

    # usual_activities_in_DB = services.getUsualActivities()
    usual_activities_in_DB_day_group = services.getListOfUsualActivitiesGroupByDay()

    if request.method == "POST":
        if child_name:
            try:
                services.setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"

        if activity_name:
            try:
                services.setActivity(
                    activity_name, activity_price, activity_time, activity_comment
                )
                message = "Activité créé"
            except:
                error = "Erreur dans la création"

        if activity_day and usual_activity:
            try:
                if int(activity_day) > 0 and int(usual_activity) > 0:
                    services.setUsualActivity(activity_day, usual_activity)
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
