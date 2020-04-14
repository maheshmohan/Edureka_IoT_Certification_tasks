from flask import Flask
import socket
import re
import json
import urllib3
from math import radians, cos, sin, asin, sqrt
from requests import get
import pprint
from haversine import haversine, Unit

app = Flask(__name__)

global latest_weather_url
latest_weather_url = "https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/"

def get_location():
    http = urllib3.PoolManager()

    url = 'http://ipinfo.io/json'

    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    
    loc = data['loc']

    loc_tuple = eval(loc)

    print (str(loc_tuple))
    
    return loc_tuple

def fetch_stations():
    url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
    stations = get(url).json()['items']
    return stations

def find_closest(all_stations, cur_loc):
    smallest = 20036
    for station in all_stations:
        station_lon = station['weather_stn_long']
        station_lat = station['weather_stn_lat']
        station_loc = (station_lat, station_lon)
        distance = haversine(station_loc, cur_loc)
        if distance < smallest:
            smallest = distance
            closest_station = station['weather_stn_id']
            print(closest_station)
    return closest_station

@app.route("/")                   
def hello():
    global latest_weather_url
    lat_long = get_location()
    stations = fetch_stations()
    closest = find_closest(stations, lat_long)
    latest_weather_url = latest_weather_url + str(1058817)
    print(latest_weather_url)
    my_weather = get(latest_weather_url).json()['items']
    if not my_weather:
        return "weather station down. Try again later."
    else:
        amb_temp = my_weather[0]['ambient_temp']
        gnd_temp = my_weather[0]['ground_temp']
        air_qual = my_weather[0]['air_quality']
        air_pres = my_weather[0]['air_pressure']
        humid = my_weather[0]['humidity']
        wind_dire = my_weather[0]['wind_direction']
        wind_speed = my_weather[0]['wind_speed']
        
        display_string = "ambient temperature : " + str(amb_temp) + "\n ground temperature : " + str(gnd_temp)    #add other parameters similarly
        
        return display_string
    #return str(my_weather)
    #return "Hello World!"

if __name__ == "__main__":        
    app.run(debug=True)                
