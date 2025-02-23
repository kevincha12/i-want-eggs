import os
import folium
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ROUTE_API_KEY")

# Create your views here.
def home_view(request):
    print(API_KEY)
    return render(request, "home.html", {"api_key": API_KEY})

def map_view(request):
    """
    Renders a Folium map. If coordinates are passed as GET parameters,
    the map will be centered at the given latitude and longitude.
    Otherwise, it falls back to a default location.
    """
    try:
        lat = float(request.GET.get("lat", 37.7749))  # default: San Francisco
        lng = float(request.GET.get("lng", -122.4194))
    except (ValueError, TypeError):
        lat, lng = 37.7749, -122.4194

    # Create a Folium map centered on the chosen (or default) coordinates
    m = folium.Map(location=[lat, lng], zoom_start=12)
    folium.Marker(
        location=[lat, lng],
        popup="Selected Location",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Get the HTML representation of the map
    map_html = m._repr_html_()

    return render(request, "map.html", {"map": map_html})