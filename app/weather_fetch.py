import requests
import pgeocode
import math
import json
from flask import Flask, render_template
from time import strftime, localtime

nomi = pgeocode.Nominatim('us')

zip_code = input("Enter zip code here: ")

# Fetching latitude and longitude based on zip code
query = nomi.query_postal_code(zip_code)
data = { "lat": query["latitude"], "lon": query["longitude"] }
latitude = str(data["lat"]).strip()
longitude = str(data["lon"]).strip()

# Fetching city name
location = query['place_name']
API_KEY="9522b86a1fd924780a88cbb326c41a47"


x = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}8&lon={longitude}&appid={API_KEY}&units=imperial')

weather_data = x.json()

print(weather_data['main'])
print()
print()
print(weather_data)
print()

app = Flask(__name__)

sunrise = strftime('%-I:%M%p', localtime(weather_data['sys']['sunrise']))
sunset = strftime('%-I:%M%p', localtime(weather_data['sys']['sunset']))
date = strftime('%Y-%m-%d', localtime(weather_data['sys']['sunset']))

print(sunrise)
print(sunset)

weather_data['sys']['sunrise'] = sunrise
weather_data['sys']['sunset'] = sunset

@app.route('/')
def hello():
    return render_template('template.html', weather=weather_data['main'], location=weather_data['name'], wind_speed=weather_data['wind']['speed'],
                           sunrise=weather_data['sys']['sunrise'], sunset=weather_data['sys']['sunset'], date=date)

if __name__ == '__main__':
    app.run()


"""
{ 'coord': {'lon': -76.9969, 'lat': 39.0669}, 
  'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 
  'base': 'stations', 'main': {'temp': 31.42, 'feels_like': 21.78, 'temp_min': 29.73, 'temp_max': 33.66, 'pressure': 1022, 'humidity': 42, 'sea_level': 1022, 'grnd_level': 1010}, 
  'visibility': 10000, 
  'wind': {'speed': 12.66, 'deg': 280, 'gust': 21.85}, 
  'clouds': {'all': 0}, 'dt': 1739843557, 
  'sys': {'type': 2, 'id': 2003404, 'country': 'US', 'sunrise': 1739793414, 'sunset': 1739832441}, 
  'timezone': -18000, 
  'id': 4351951, 
  'name': 'Colesville', 
  'cod': 200
  }
"""









