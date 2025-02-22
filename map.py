import json
import folium
import polyline

with open("data/route.json", "r") as f:
    data = json.load(f)

overview_polyline = data["routes"][0]["overview_polyline"]["points"]

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


m.save("data/map.html")
print("done: saved to map.html")