import requests
import pgeocode
import math

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