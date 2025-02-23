import math

def calculate_distance(origin, lat2, lon2):
    lat1, lon1 = map(float, origin.split(","))
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    radius = 3958.8
    distance = radius * c
    return distance


def get_stores_in_radius(origin, stores):
    min_distance = float('inf')

    distances = []
    for store in stores:
        distance = calculate_distance(origin, store.latitude, store.longitude)
        distances.append([store, distance])
        if distance < min_distance:
            min_distance = distance
    radius = min_distance+1

    return [[store, distance] for store, distance in distances if distance <= radius]
        

def get_min_price_location(origin, stores, mileage, gas_price):
    good_stores = get_stores_in_radius(origin, stores)
    min_price = float('inf')
    cheapest_egg = {}
    cheapest_store = None

    for s in good_stores:
        fuel_price = mileage*gas_price*s[1]
        cheap_egg = min(s.eggs, key=lambda d: next(iter(d.values())))
        total_price = fuel_price + cheap_egg.values()[0]
        if total_price < min_price:
            min_price = total_price
            cheapest_egg = cheap_egg
            cheapest_store = s
    
    return cheapest_store


        


