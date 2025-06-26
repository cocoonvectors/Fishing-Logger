from flask import Flask, request,render_template,redirect, flash,session, jsonify
from functools import wraps
from werkzeug.security import check_password_hash,generate_password_hash
from dotenv import load_dotenv
import sqlite3
import os
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def logged_in(func):#check user is logged in
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "userId" not in session:
            return redirect("/")
        else: 
            return func(*args,**kwargs)
    return wrapper

@app.route("/home")
@logged_in
def Welcome():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])

def register():
    if request.method == "POST":
        # make sure an account doesnt already exist
        # if exists throw error
        username =  request.form.get("username")
        with sqlite3.connect("fishing.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (username,))
            row = cursor.fetchone()
            if row: #if user exists 
                flash("User already exists.","exists")
                return redirect("/register")
            else: #logging new user into db
                password = generate_password_hash(request.form.get("password")) # hash password
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                conn.commit()
                flash("Registered! Please login with your new account","regLogout")
                return redirect("/")
    return render_template("register.html")


@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        with sqlite3.connect("fishing.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id,username,password FROM users WHERE LOWER(username) = LOWER(?)", (username,))
            row = cursor.fetchone()
            if row: #if user exists 
                verifyPassword = check_password_hash(row["password"],request.form.get("password"))
                if verifyPassword:
                    session["userId"] = row["id"]
                    return redirect("/accounthome")                
                else:
                    flash("Wrong Username or Password please try again.","wrong")
            else: #logging new user into db
                flash("Username doesn't exist please register.","wrong")
                return redirect("/register")
    return render_template("login.html")

@app.route("/accounthome")
@logged_in
def accountHome():
    return render_template("accounthome.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.","regLogout")
    return redirect("/")

@app.route("/log", methods=["GET", "POST"])
@logged_in
def Log():
    if request.method == "POST":
        # Handle the form submission here
        name = request.form.get("species")

        #checking if species is in db or if we need to add it
        id = getSpeciesId(name)

        temperature = request.form.get("temperature")
        latlong = request.form.get("latlong")
        condition = request.form.get("cloud_cover")
        humidity = request.form.get("humidity")
        wind = request.form.get("wind_speed")
        lunarphase = request.form.get("lunar_phase")
        date = request.form.get("date")
        location = request.form.get("location")
        time = request.form.get("time")
        
        insertTrip(session["userId"],id,latlong,location,date,time,temperature,condition,humidity,wind,lunarphase)

        flash("Trip logged","logged") #just a popup to let the user know their catch is saved
        return redirect("/log")
    return render_template("log.html")

@app.route("/trips")
@logged_in
def trips():
    trips = getTrips()
    species = request.args.get("species")
    if species:
        filteredtrips = []
        for trip in trips:
            if trip["species"].lower() == species.lower(): 
                filteredtrips.append(trip)
        return render_template("trips.html", trips=filteredtrips)    
    return render_template("trips.html", trips=trips)

@app.route("/delete/<int:trip_id>",methods=["POST"])
@logged_in
def delete(trip_id):
    with sqlite3.connect("fishing.db") as conn:
        conn.execute("""
                        DELETE FROM trips 
                        where id = ? 
                     """,
                        (trip_id,))
        conn.commit()
 
    flash("Deleted Catch","deleted")
    return redirect("/trips")

def insertTrip (user_id,species_id,latlong,location,date,time,temperature,cloud_cover,humidity,wind_speed,lunar_phase):
       with sqlite3.connect("fishing.db") as conn:
            conn.execute("""
                         INSERT INTO trips(
                            user_id, species_id,latlong,location,date,time,
                            temperature,cloud_cover,humidity,
                            wind_speed,lunar_phase
                         ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            user_id,species_id,latlong,location,
                            date,time,temperature,
                            cloud_cover,humidity,wind_speed,lunar_phase
                         ))
            conn.commit()

def getSpeciesId(name):
    with sqlite3.connect("fishing.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM species WHERE LOWER(name) = LOWER(?)", (name,))
        row = cursor.fetchone()
        if row: #if species exists 
            return row[0]  
        else: #logging new species not in db
            #Sqlite will generate unique id to new species inserted
            cursor.execute(
                "INSERT INTO species (name, common_name,lang, region) VALUES (?, ?, ?,?)",
                (name, name,"user-submitted", "user-submitted")
            )
            return cursor.lastrowid

def getTrips():
           with sqlite3.connect("fishing.db") as conn:
            print(session["userId"])
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
                        select trips.id,
                            species.name as species_name,
                            trips.location,
                            trips.date,
                            trips.time,
                            trips.temperature,
                            trips.cloud_cover,
                            trips.humidity,
                            trips.wind_speed,
                            trips.lunar_phase 
                        from trips
                        inner join species ON trips.species_id = species.id
                        where user_id = ?
                        """,(session["userId"],))
            rows = cur.fetchall()
            trips = []
            for row in rows:
                trips.append({
                    "trip_id" : row["id"],
                    "species" : row["species_name"],
                    "location" : row["location"],
                    "date" :row["date"],
                    "time" :row["time"],
                    "temperature" :row["temperature"],
                    "condition" :row["cloud_cover"],
                    "humidity" :row["humidity"],
                    "wind" :row["wind_speed"],
                    "lunarphase" :row["lunar_phase"]
                })
            return trips
           

@app.route("/api/weather",methods=["POST"])
def get_weather():
    data = request.get_json()
    lat = str(data.get("lat"))
    lon = str(data.get("lon"))
    apikey = os.getenv('WEATHER_API_KEY')
    if not lat or not lon:
        return jsonify({"error": "Missing lat, lon, or date"}), 400

    weatherUrl = "https://api.weatherapi.com/v1/current.json?key="+ apikey +"&q="+ lat + "," + lon

    response = requests.get(weatherUrl)
    weather_data = response.json()
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500
    return jsonify(weather_data)

@app.route("/api/histweather",methods=["POST"])
def get_histweather():
    data = request.get_json()
    lat = str(data.get("lat"))
    lon = str(data.get("lon"))
    date = data.get("date")
    apikey = os.getenv('WEATHER_API_KEY')
    if not lat or not lon or not date:
        return jsonify({"error": "Missing lat, lon, or date"}), 400

    weatherUrl = "https://api.weatherapi.com/v1/history.json?key="+ apikey +"&q="+ lat + "," + lon + "&dt=" + date

    response = requests.get(weatherUrl)
    weather_data = response.json()
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    return jsonify(weather_data)

@app.route("/api/geocode",methods=["POST"])
def get_geocode():
    data = request.get_json()
    lat = str(data.get("lat"))
    lon = str(data.get("lon"))
    if not lat or not lon:
        return jsonify({"error": "Missing lat, lon, or date"}), 400

    apikey = os.getenv('GEOCODE_API_KEY')

    geocodeURL = "https://api.opencagedata.com/geocode/v1/json?q=" + lat + "+" + lon + "&key=" + apikey + ";"

    response = requests.get(geocodeURL)
    geocode_data = response.json()
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    return jsonify(geocode_data)

@app.route("/api/astro",methods=["POST"])
def get_astro():
    data = request.get_json()
    lat = str(data.get("lat"))
    lon = str(data.get("lon"))
    date = data.get("date")
    if not lat or not lon or not date:
        return jsonify({"error": "Missing lat, lon, or date"}), 400

    apikey = os.getenv('WEATHER_API_KEY')

    weatherUrl = "https://api.weatherapi.com/v1/astronomy.json?key="+ apikey +"&q="+ lat + "," + lon + "&dt=" + date

    response = requests.get(weatherUrl)
    weather_data = response.json()
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)
