import os
import board
import busio
import time
import math

# Initialise UART
uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=0)
counter = 0


airports = "airports_short.csv"
fixes = "fixes_short.csv"
routes = "routes.csv"

# region Fetching airport coordinates from the .csv file by entering the airport ICAO identifier
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
# endregion

# region Fetching the coordinates of fixes from the .csv file by entering their unique, 5 letter identifier
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
