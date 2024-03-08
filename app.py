from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from datetime import datetime
from services.services_activity import (
    getActivities,
    deleteActivity,
    updateActivity,
    setActivity,
    checkNotExistingActivityByName,
)
from services.services_child import getChilds, updateChild, deleteChild, setChild
from services.services_usual_activity import (
    getChilds,
    get_list_of_usual_activities_group_by_day,
    getUsualActivities,
    setUsualActivity,
    setUsualActivityForAllChildren,
    deleteUsualActivityByActivityName,
)
from services.services_month_activities import (
    get_months_with_details,
    set_month_activity,
    set_month_activity_for_all_children, get_activities_price_by_month_group_by_child_activity,set_day_off_on_activity, delete_month_and_activities)
from services.services_off_days import set_off_days
from classes.JoursFeriesClass import JoursFeries, School_day, Jour, Mois
from classes.MonthActivities import MonthActivities
from functions_help import stringToNumber, month_days


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

bootstrap = Bootstrap5(app)

isInEditionMode = False
error = None
message = None
error_date = None


@app.route("/", methods=["POST", "GET"])
def index():
    month = (request.form.get("month-select"),)
    year = (request.form.get("year"),)
    set_month_with_usual_activities = request.form.get(
        "set_month_with_usual_activities"
    )

    school_details_months = get_months_with_details()
    childrenInDb = getChilds()
    activitiesInDb = getActivities()
    usual_activities_in_DB = getUsualActivities()

    month_canceled_type = ["absence enfant", "grève", "annulation par école"]
    if request.method == "POST":
        try:
            mymonthActivities = MonthActivities(year[0], Mois[month[0]])
            mymonthActivities.set_month()
            if set_month_with_usual_activities == "on":
                mymonthActivities.set_activities_from_usual_activities()
        except:
            error = "Erreur dans la création"

    return render_template(
        "home.html",
        today=datetime.today(),
        Mois=Mois,
        error_date=error_date,
        school_months=school_details_months,
        childrenInDb=childrenInDb,
        activitiesInDb=activitiesInDb,
        usual_activities_in_DB=usual_activities_in_DB,
        month_canceled_type=month_canceled_type,
    )


@app.route("/day_off_create", methods=["POST", "GET"])
def day_off_create():
    global error
    global message

    input_date_str = request.form.get("input_date")
    input_date = datetime.strptime(input_date_str, "%Y-%m-%d").date()

    activity_child_id = request.form.get("activity_child")
    activity_id = request.form.get("activity")
    activity_web_validation = request.form.get("activity_web_validation")
    day_off_web_validation = request.form.get("day_off_web_validation")
    month_canceled_type = request.form.get("month_canceled_type")

    if request.method == "POST":
        mymonthActivities = MonthActivities(input_date.year, input_date.month)
        if mymonthActivities.check_month_school_date(input_date):
            if int(activity_id) > 0:
                mymonthActivities.set_month()
                if int(activity_child_id) > 0:
                    set_month_activity(
                        input_date,
                        activity_id,
                        activity_child_id,
                        0,
                        activity_web_validation,
                    )
                else:
                    set_month_activity_for_all_children(
                        input_date, activity_id, 0, activity_web_validation
                    )

            elif month_canceled_type == "grève":
                    set_off_days(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=1)
                    set_day_off_on_activity(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=1)
            elif month_canceled_type == "absence enfant":
                    set_off_days(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=0, family_canceled=1)
                    set_day_off_on_activity(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=0, family_canceled=1)
            elif month_canceled_type == "annulation par école":
                    set_off_days(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=0, family_canceled=0, school_canceled=1)
                    set_day_off_on_activity(input_date, int(activity_child_id), day_off_web_validation, strike_canceled=0, family_canceled=0, school_canceled=1)
        else:
            error_date = "La date choisie n'est pas un jour d'école"
            # TODO a GERER les erreurs et surtout informer cette erreur de date !! Attention a ne pas mettre sur le même jour une absence+greve+annulation

    return redirect("/")


@app.route("/mois/<int:item_id>", methods=["POST"])
def mois(item_id):
    
    month_year = request.form.get("month_year")
    month = request.form.get("month")
    total_price_activities = request.form.get("price_activities")

    month_prices_details = get_activities_price_by_month_group_by_child_activity(int(month_year), int(month))
    # print('--PRICE',month_prices_details)
    
    return render_template("month.html", month_id=item_id , Jour=Jour, Mois=Mois, mymonthActivities = MonthActivities(month_year, month), stringToNumber=stringToNumber, month_prices_details=month_prices_details, total_price_activities=total_price_activities)

@app.route("/mois/supprimer/<int:item_id>", methods=["POST"])
def supprimer_mois(item_id):
    
    month_year = request.form.get("month_year")
    month = request.form.get("month")
    
    print("--SUPPRIMEr--mois ", item_id, month_year, month)
    delete_month_and_activities(int(item_id), int(month_year), int(month))
    
    return redirect("/")

@app.route("/mode_edition", methods=["POST"])
def mode_edition():
    global isInEditionMode
    template_redirection = request.form.get("template_redirection")
    if request.method == "POST":
        if isInEditionMode is False:
            isInEditionMode = True
        else:
            isInEditionMode = False
    return redirect(template_redirection)


@app.route("/child_delete/<int:item_id>", methods=["POST"])
def child_delete(item_id):
    if request.method == "POST":
        deleteChild(item_id)
    return redirect("/params")


@app.route("/child_update/<int:item_id>", methods=["POST", "GET"])
def child_update(item_id):
    new_child_name = request.form.get("new_child_name")
    if request.method == "POST":
        updateChild(item_id, new_child_name)
    return redirect("/params")


@app.route("/child_create", methods=["POST"])
def child_create():
    global error
    global message

    child_name = request.form.get("child_name")

    if request.method == "POST":
        if child_name:
            try:
                setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"
    return redirect("/params")


@app.route("/activity_delete/<int:item_id>", methods=["POST"])
def activity_delete(item_id):
    if request.method == "POST":
        deleteActivity(item_id)
    return redirect("/params")


@app.route("/activity_update/<int:item_id>", methods=["POST", "GET"])
def activity_update(item_id):
    new_activity = {
        "name": request.form.get("new_activity_name"),
        "time": request.form.get("new_activity_time"),
        "price": request.form.get("new_activity_price"),
        "comment": str(request.form.get("new_activity_comment")),
    }
    if request.method == "POST":
        updateActivity(item_id, new_activity)
    return redirect("/params")


@app.route("/activity_create", methods=["POST"])
def activity_create():
    global error
    global message

    activity = {
        "name": request.form.get("activity_name"),
        "time": request.form.get("activity_time"),
        "price": request.form.get("activity_price"),
        "comment": request.form.get("activity_comment"),
    }

    if request.method == "POST":
        if activity["name"]:
            try:
                if checkNotExistingActivityByName(activity["name"]):
                    setActivity(activity)
                    message = "Activité créé"
                else:
                    error = "Nom déjà existant"
            except:
                error = "Erreur dans la création"

    return redirect("/params")


@app.route("/usual_activity_delete/<int:item_id>", methods=["POST"])
def usual_activity_delete(item_id):
    activity_name = request.form.get("usual_activity_name")
    if request.method == "POST":
        deleteUsualActivityByActivityName(item_id, activity_name)
    return redirect("/params")


@app.route("/usual_activity_create", methods=["POST"])
def usual_activity_create():
    global error
    global message

    usual_activity = {
        "day": request.form.get("activity_day"),
        "activity": request.form.get("usual_activity"),
        "child": request.form.get("usual_activity_child"),
    }

    if request.method == "POST":
        if usual_activity["day"] and usual_activity["activity"]:
            try:
                if (
                    int(usual_activity["day"]) > 0
                    and int(usual_activity["activity"]) > 0
                    and int(usual_activity["child"]) > 0
                ):
                    setUsualActivity(usual_activity)
                    message = "Activité créé"
                elif (
                    int(usual_activity["day"]) > 0
                    and int(usual_activity["activity"]) > 0
                    and int(usual_activity["child"]) == 0
                ):
                    setUsualActivityForAllChildren(usual_activity)
                    message = "Activité créé"
            except:
                error = "Erreur dans la création"

    return redirect("/params")


@app.route("/params", methods=["POST", "GET"])
def params():
    global error
    global message
    global isInEditionMode

    childrenInDb = getChilds()
    activitiesInDb = getActivities()

    if getUsualActivities():
        usual_activities_in_DB_day_group = get_list_of_usual_activities_group_by_day()
    else:
        usual_activities_in_DB_day_group = []
            
    JoursFeriesAnneeEnCours = JoursFeries()

    return render_template(
        "params.html",
        message=message,
        error=error,
        childrenInDb=childrenInDb,
        activitiesInDb=activitiesInDb,
        JoursFeriesAnneeEnCours=JoursFeriesAnneeEnCours.dumps(),
        usual_activities_in_DB=usual_activities_in_DB_day_group,
        Jour=School_day,
        stringToNumber=stringToNumber,
        isInEditionMode=isInEditionMode,
    )


if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=True)
    # flask run --debug