import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv('ROUTE_API_KEY')

endpoint = 'https://maps.googleapis.com/maps/api/directions/json'
params = {
    "origin": "40.712776,-74.005974",
    "destination": "40.730610,-73.935242",
    "key": api_key
}

response = requests.get(endpoint, params)
if response.status_code == 200:
    data = response.json()
    with open("output.json", "w") as file:
        json.dump(data, file, indent=4) 
    print("Route data:", data)
else:
    print("Error:", response.status_code, response.text)
