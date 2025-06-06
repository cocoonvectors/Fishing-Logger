# A **Fishing Logger:**<br/>
  This is a small hobby project I made to log my fishing catches.
  
  The goal is to eventually release it for free on both mobile and web. I built it to create a local journal of your fishing trips and to keep your private fishing spots safe.
  
  Right now, the app can track the location, weather, and date/time of your catches.
  
  I have a lot planned for this project as I continue working on it. One feature I’m especially excited to add is the ability to upload photos of your catch and use LLMs to recognize the species automatically. The goal is to make logging a catch as quick and easy as possible so you can get more casts in!

**API Keys Required:**

  To use the current features, you’ll need your own API keys for:<br/>
  - OpenCage Geocoding<br/>
  - WeatherAPI
  
  Store them in the .env file like this:<br/>
  GEOCODE_API_KEY=your_geocode_key<br/>
  WEATHER_API_KEY=your_weatherapi_key<br/>
  SECRET_KEY=your_flask_secret<br/>

**APIs:**<br/>
	- WeatherAPI for current, historical, and astronomy data<br/>
	- OpenCage Geocoding

**Tech Stack:**<br/>
  - Backend: Python, Flask, SQLite<br/>
  - Frontend: HTML, CSS, JavaScript, Leaflet.js

**To run this locally:**<br/>
  Go ahead and clone the repo, pip install dependencies and run app.py

As of now there are no plans to make this a commercial product.

**Here are the relevant organizations that I have used so far for the project:**<br/>
  - Map tiles provided by OpenStreetMap<br/>
  - Geocoding powered by OpenCage Data<br/>
  - Weather and astronomy data provided by WeatherAPI.com<br/>
  - Fish species dataset inspired by data from gbif.org


