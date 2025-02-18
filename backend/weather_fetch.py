import requests
import pgeocode
import math
import json
from flask import Flask, render_template
from time import strftime, localtime
import os
from dotenv import load_dotenv

load_dotenv()

# Purpose of this class: handle user input
class PromptHandler:
    def __init__(self):
        self = self
    def get_zip_code():
        return input("Enter zip code here: ")

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def call_api_url(self):
        return requests.get(self.base_url)

nomi = pgeocode.Nominatim('us')

x = PromptHandler.get_zip_code()

# Parsing geocode API Data
query = nomi.query_postal_code(x)
data = { "lat": query["latitude"], "lon": query["longitude"] }
latitude = str(data["lat"]).strip()
longitude = str(data["lon"]).strip()
location = query['place_name']
API_KEY = os.getenv('API_KEY')

client = APIClient(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}8&lon={longitude}&appid={API_KEY}&units=imperial')

# Calling and JSON-ify the Weather API data
x = client.call_api_url()
weather_data = x.json()


# Parsing the Weather API data
sunrise = strftime('%-I:%M%p', localtime(weather_data['sys']['sunrise']))
sunset = strftime('%-I:%M%p', localtime(weather_data['sys']['sunset']))
date = strftime('%Y-%m-%d', localtime(weather_data['sys']['sunset']))
weather_data['sys']['sunrise'] = sunrise
weather_data['sys']['sunset'] = sunset

# Start of flask process
app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('template.html', weather=weather_data['main'], location=weather_data['name'], wind_speed=weather_data['wind']['speed'],
                           sunrise=weather_data['sys']['sunrise'], sunset=weather_data['sys']['sunset'], date=date)

if __name__ == '__main__':
    app.run()