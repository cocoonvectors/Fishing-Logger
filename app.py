from flask import Flask, request,render_template,redirect
import json

import flask

app = Flask(__name__)
app.secret_key = "32131234"
@app.route("/")

def Welcome():
    return render_template("home.html")


@app.route("/log", methods=["GET", "POST"])

def Log():
    if request.method == "POST":
        # Handle the form submission here
        trip = {
            "species": request.form.get("species"),
            "weather": request.form.get("location"),
            "location": request.form.get("weather"),
            "time": request.form.get("time")
        }   
        try:
            with open("log.json", "r") as f: #try to load json
                trips = json.load(f)
        except FileNotFoundError: #if no json create new list
                trips = []


        trips.append(trip)
        with open("log.json", "w") as f:
             json.dump(trips, f, indent=4)
        flask.flash("Trip logged")
        return redirect("/log")
    return render_template("log.html")

@app.route("/trips")

def trips():
    try:
        with open("log.json", "r") as f: #try to load json
                trip_data = json.load(f)
    except FileNotFoundError:
        trip_data = []
    return render_template("trips.html", trips=trip_data)

@app.route("/delete/<int:index>",methods=["POST"])
def delete(index):
    try:
        with open("log.json","r") as f:
           trips = json.load(f)
    except FileNotFoundError:
        trips = []

    if 0 <= index < len(trips):
        del trips[index]
        with open("log.json","w") as f:
            json.dump(trips, f, indent=4)
    flask.flash("Deleted Catch")
    return redirect("/trips")

if __name__ == "__main__":
    app.run(debug=True)
