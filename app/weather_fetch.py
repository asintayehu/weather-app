import requests
import pgeocode
import math
import json
from flask import Flask, render_template
from time import strftime, localtime
import os
from dotenv import load_dotenv

load_dotenv()

nomi = pgeocode.Nominatim('us')

zip_code = input("Enter zip code here: ")

# Fetching latitude and longitude based on zip code
query = nomi.query_postal_code(zip_code)
data = { "lat": query["latitude"], "lon": query["longitude"] }
latitude = str(data["lat"]).strip()
longitude = str(data["lon"]).strip()

# Fetching city name
location = query['place_name']

API_KEY = os.getenv("API_KEY")

x = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}8&lon={longitude}&appid={API_KEY}&units=imperial')

weather_data = x.json()

app = Flask(__name__)

sunrise = strftime('%-I:%M%p', localtime(weather_data['sys']['sunrise']))
sunset = strftime('%-I:%M%p', localtime(weather_data['sys']['sunset']))
date = strftime('%Y-%m-%d', localtime(weather_data['sys']['sunset']))

weather_data['sys']['sunrise'] = sunrise
weather_data['sys']['sunset'] = sunset

@app.route('/')
def hello():
    return render_template('template.html', weather=weather_data['main'], location=weather_data['name'], wind_speed=weather_data['wind']['speed'],
                           sunrise=weather_data['sys']['sunrise'], sunset=weather_data['sys']['sunset'], date=date)

if __name__ == '__main__':
    app.run()