import os

airports = "airports_short.csv"
fixes = "fixes_short.csv"
routes = "routes.csv"


def fetch_airport_coordinates(icao):
    with open(airports, "r") as file:
        next(file)
        for line in file:
            parts = line.strip().split(';')
            if parts[0] == icao.upper():
                lat = parts[9]
                long = parts[10]
                print(lat, long)
                break
            else:
                continue

def fetch_fix_coordinates(id):
    with open(fixes, "r") as file:
        next(file)
        for line in file:
            parts = line.strip().split(';')
            if parts[0] == id.upper():
                lat = parts[1]
                long = parts[2]
                print(lat, long)
                break
            else:
                continue
