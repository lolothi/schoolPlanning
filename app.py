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
    """Child creation"""
    error = None
    message = None
    child_name = request.form.get("child_name")

    childsInDb = services.getChilds()

    if request.method == "POST":
        if child_name:
            try:
                services.setChild(child_name)
                message = "Enfant créé"
            except:
                error = "Erreur dans la création"

    return render_template("params.html", message=message, error=error, childsInDb=childsInDb, child_name=child_name)

if __name__ == '__main__':
    app.run(debug=True)