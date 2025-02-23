import os
import requests
import folium
import polyline
from dotenv import load_dotenv
import json
from django.shortcuts import render
from django.conf import settings
import controller 

load_dotenv()
api_key = os.getenv("ROUTE_API_KEY")


def home_view(request):
    """
    Render the home page with the Google Maps autocomplete search box.
    The API key is passed to the template for loading the Google Maps API.
    """
    return render(request, "home.html", {"api_key": api_key})


def route_view(request):
    """
    Use the origin coordinates from the Google search on the home page to call the Google Directions API.
    Draw the route from the selected origin to the fixed destination and display it using a Folium map.
    Also, retrieve the mileage value for later calculations.
    """
    # Get the origin from the GET parameters (expected format: "lat,lng")
    origin = request.GET.get("origin")
    mileage = request.GET.get("mileage")
    gas_price = request.GET.get("gas_price")
    if not origin or not mileage or not gas_price:
        return render(request, "error.html", {"message": "Origin or mileage not provided."})

    destination = "40.730610,-73.935242"  # fixed destination








    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        # with open("output.json", "w") as file:
        #     json.dump(data, file, indent=4) 
        try:
            overview_polyline = data["routes"][0]["overview_polyline"]["points"]
            distance = data["routes"][0]["legs"][0]["distance"]["value"] #in meters
        except (KeyError, IndexError):
            return render(request, "error.html", {"message": "No route found for the given origin."})
    else:
        return render(request, "error.html", {"message": f"Error fetching route: {response.status_code} {response.text}"})

    decoded_points = polyline.decode(overview_polyline)
    start_lat, start_lng = decoded_points[0]
    end_lat, end_lng = decoded_points[-1]

    m = folium.Map(location=[start_lat, start_lng], zoom_start=12)
    folium.PolyLine(decoded_points, color="blue", weight=5, opacity=0.8).add_to(m)
    folium.Marker(
        location=[start_lat, start_lng],
        popup="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)
    folium.Marker(
        location=[end_lat, end_lng],
        popup="Finish",
        icon=folium.Icon(color="red")
    ).add_to(m)

    map_html = m._repr_html_()

    print("Mileage received:", mileage)  # or perform additional processing

    return render(request, "map.html", {"map": map_html})


