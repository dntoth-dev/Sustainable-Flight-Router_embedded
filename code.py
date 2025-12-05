import os
# import board
# import busio
import time
import math

# Initialise UART
# uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=0)
# counter = 0

airports = "airports_short.csv"
fixes = "fixes_short.csv"
routes = "routes.csv"

# region Fetch latitude of airports/navaids
def lat(id):
    if len(id) == 4: # Airports have a 4 letter identifier (luckily that's an easy difference to spot lets goo)
        icao = id
        with open(airports, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == icao.upper():
                    lat = parts[9]
                    return lat
                else:
                    continue
    elif len(id) == 5: # Fixes have a 5 letter identifier
        navaid = id
        with open(fixes, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == navaid.upper():
                    lat = parts[1]
                    # A formula converting DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees) format, because in the fixes_short.csv, coordinates are provided like that
                    prefix = ""
                    if lat[0] == 'S':
                        prefix = '-'
                    if lat[1] != 0:
                        deg = lat[1] + lat[2]
                    else:
                        deg = lat[2]
                    min = lat[3] + lat[4]
                    sec = lat[5] + lat[6]
                    dec_deg = int(deg) + int(min)/60 + int(sec)/3600
                    lat_dec_deg = f"{prefix}{dec_deg}"
                    return lat_dec_deg
                else:
                    continue
    else:
        print("Please enter a 4 letter ICAO or a 5 letter NAVAID!\nNOTE: THE PROGRAM WORKS FOR EUROPEAN ROUTES ONLY!")

# endregion
# region Fetch longitude of airports/navaids
def long(id):
    if len(id) == 4: # Airports have a 4 letter identifier (luckily that's an easy difference to spot lets goo)
        icao = id
        with open(airports, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == icao.upper():
                    long = parts[10]
                    return long
                else:
                    continue
    elif len(id) == 5: # Fixes have a 5 letter identifier
        navaid = id
        with open(fixes, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == navaid.upper():
                    long = parts[2]
                    # A formula converting DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees) format, because in the fixes_short.csv, coordinates are provided like that
                    prefix = ""
                    if long[0] == 'W':
                        prefix = '-'
                    if long[1] != 0:
                        deg = long[1] + long[2] + long[3]
                    else:
                        deg = long[2] + long[3]
                    min = long[4] + long[5]
                    sec = long[6] + long[7]
                    dec_deg = int(deg) + int(min)/60 + int(sec)/3600
                    long_dec_deg = f"{prefix}{dec_deg}"
                    return long_dec_deg
                else:
                    continue
    else:
        print("Please enter a 4 letter ICAO or a 5 letter NAVAID!\nNOTE: THE PROGRAM WORKS FOR EUROPEAN ROUTES ONLY!")
# endregion

# One list will store all the routes, each list element is a route
default_routes = []

# Opening routes.csv, going through elements of routes. Includes element logic, which filters against empty cells
with open(routes, "r") as file:
    next(file)
    for line in file:
        current_route = []
        parts = line.strip().split(';')
        for piece in parts:
            if piece.isalpha(): # Exclude empty cells
                current_route.append(piece)
        default_routes.append(current_route)

deps = [] # List for all departure airports
arrs = [] # List for all arrival airports

for route in default_routes:
    deps.append(route[0])
    arrs.append(route[len(route)-1])
    
EARTH_RADIUS_KM = 6371.0088
    
# Distance calculation with this function (original name: haversine_distance_wgs84)
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points 
    (given in decimal degrees) on the surface of the Earth using 
    the Haversine formula with the WGS-84 mean radius.
    
    This is a simplification that is highly accurate for distances 
    up to a few hundred kilometers and provides a good compromise 
    on the Pico W.
    """
    
    # 1. Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    # 2. Calculate the difference in latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # 3. Apply the Haversine formula components:
    
    # Haversine part (a)
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    
    # Angular distance part (c) = 2 * atan2(math.sqrt(a), math.sqrt(1 - a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 4. Calculate the distance (Distance = Radius * c)
    distance = EARTH_RADIUS_KM * c
    
    return distance    

# Calculate aircraft bearing with this function
def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    
    y = math.sin(dlon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    
    # Bearing in radians, then convert to degrees and normalize (0 to 360)
    bearing_rad = math.atan2(y, x)
    bearing_deg = math.degrees(bearing_rad)
    
    return (bearing_deg + 360) % 360

