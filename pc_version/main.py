from geopy.distance import geodesic

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
    elif len(id) == 5: # Fixes have a 5 letter identifier
        navaid = id
        with open(fixes, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == navaid.upper():
                    lat = parts[1]
                    # A formula converting DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees) format, because in the fixes_short.csv, coordinates are provided like that
                    prefix = '-' if lat[0] == 'S' else ''
                    deg = lat[1:3]
                    min = lat[3:5]
                    sec = lat[5:7]
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
    elif len(id) == 5: # Fixes have a 5 letter identifier
        navaid = id
        with open(fixes, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(';')
                if parts[0] == navaid.upper():
                    long = parts[2]
                    # A formula converting DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees) format, because in the fixes_short.csv, coordinates are provided like that
                    prefix = '-' if long[0] == 'W' else ''
                    deg = long[1:4]
                    min = long[4:6]
                    sec = long[6:8]
                    dec_deg = int(deg) + int(min)/60 + int(sec)/3600
                    long_dec_deg = f"{prefix}{dec_deg}"
                    return long_dec_deg
    else:
        print("CoordinateError: An invalid ICAO/NAVAID was provided, or its coordinates cannot be called.")
# endregion