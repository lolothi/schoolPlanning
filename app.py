from flask import Flask, render_template, request, redirect
from datetime import datetime
from functions_help import stringToNumber
import services_activity
import services_child
import services_usual_activity
import services_month_activities
from classes.JoursFeriesClass import JoursFeries, Jour, Mois
from classes.MonthActivities import MonthActivities
import functions_help


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

isInEditionMode = False
error = None
message = None

@app.route("/", methods=["POST", "GET"])
def index():

    month = request.form.get("month-select"),
    year = request.form.get("year"),
    set_month_with_usual_activities = request.form.get("set_month_with_usual_activities")
    
    school_details_months = services_month_activities.get_months_with_details()
    # print('JOURS OUVRES', functions_help.month_business_days(2024, 5))
    # print('JF_sur joursOUVRé', functions_help.month_holidays_closed(2024, 5))
    # print('holidays', functions_help.holidays(2024, 1))
    if request.method == "POST":

        try:
            mymonthActivities = MonthActivities(year[0], Mois[month[0]])
            mymonthActivities.set_month()
            if set_month_with_usual_activities == 'on':
                mymonthActivities.set_usual_activities()
        except:
            error = "Erreur dans la création"

    return render_template("home.html", today=datetime.today(), Mois=Mois, school_months=school_details_months)

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
        services_child.deleteChild(item_id)   
    return redirect("/params")

@app.route('/child_update/<int:item_id>', methods=["POST", "GET"])
def child_update(item_id):
    new_child_name = request.form.get("new_child_name")
    if request.method == "POST":
        services_child.updateChild(item_id, new_child_name)
    return redirect("/params")

@app.route('/child_create', methods=["POST"])
def child_create():
    global error
    global message

    child_name = request.form.get("child_name")

    if request.method == "POST":
        if child_name:
            try:
                services_child.setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"
    return redirect("/params")

@app.route('/activity_delete/<int:item_id>', methods=["POST"])
def activity_delete(item_id):
    if request.method == "POST":
        services_activity.deleteActivity(item_id)   
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
        services_activity.updateActivity(item_id, new_activity)
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
                if services_activity.checkNotExistingActivityByName(activity['name']):
                    services_activity.setActivity(activity)
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
        services_usual_activity.deleteUsualActivityByActivityName(item_id, activity_name)   
    return redirect("/params")

@app.route('/usual_activity_create', methods=["POST"])
def usual_activity_create():
    global error
    global message

    usual_activity = {
        'day' : request.form.get("activity_day"),
        'activity' : request.form.get("usual_activity"),
        'child' : request.form.get("usual_activity_child")
    }

    if request.method == "POST":
        if usual_activity['day'] and usual_activity['activity']:
            try:
                if int(usual_activity['day']) > 0 and int(usual_activity['activity']) > 0 and int(usual_activity["child"]) > 0:
                    services_usual_activity.setUsualActivity(usual_activity)
                    message = "Activité créé"
                elif int(usual_activity['day']) > 0 and int(usual_activity['activity']) > 0 and int(usual_activity["child"]) == 0:

                    services_usual_activity.setUsualActivityForAllChildren(usual_activity)
                    message = "Activité créé"
            except:
                error = "Erreur dans la création"

    return redirect("/params")

@app.route("/params", methods=["POST", "GET"])
def params():
    global error
    global message
    global isInEditionMode

    childrenInDb = services_child.getChilds()
    activitiesInDb = services_activity.getActivities()
    if services_usual_activity.getUsualActivities():
        usual_activities_in_DB_day_group = services_usual_activity.getListOfUsualActivitiesGroupByDay()
    else:
        usual_activities_in_DB_day_group = []
 

    JoursFeriesAnneeEnCours = JoursFeries()
    # print('JF_list', JoursFeriesAnneeEnCours.to_list())
    # print('JF_str', JoursFeriesAnneeEnCours.__str__)
    # print('JF_repr', JoursFeriesAnneeEnCours.__repr__)
    # print('JF_dumps', JoursFeriesAnneeEnCours.dumps())
    # print('JF_tuple', JoursFeriesAnneeEnCours.to_namedtuple())
    

    return render_template(
        "params.html",
        message=message,
        error=error,
        childrenInDb=childrenInDb,
        activitiesInDb=activitiesInDb,
        JoursFeriesAnneeEnCours=JoursFeriesAnneeEnCours.dumps(),
        usual_activities_in_DB=usual_activities_in_DB_day_group,
        Jour=Jour,
        stringToNumber=functions_help.stringToNumber,
        isInEditionMode=isInEditionMode   )


if __name__ == "__main__":
    app.run(debug=True)
