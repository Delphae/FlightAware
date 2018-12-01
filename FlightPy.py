#!/usr/bin/env python
# coding: utf-8

#    ____       _       _
#   |  _ \  ___| |_ __ | |__   __ _  ___
#   | | | |/ _ \ | '_ \| '_ \ / _` |/ _ \
#   | |_| |  __/ | |_) | | | | (_| |  __/
#   |____/ \___|_| .__/|_| |_|\__,_|\___|
#                |_|


import requests
from datetime import datetime as dt

__version__ = "1.1"
__date__    = "2018-12-01"

def readjson(method, params, auth):
    url = "https://flightxml.flightaware.com/json/FlightXML3/"
    response = requests.get(url+method, params=params, auth=auth)
#    print response.url
    return response.json()


class FlightResult:
    def __init__(self, result=dict()):
        self.__dict__ = result

class FlightInfo:
    def __init__(self, info=dict()):
        self.__dict__ = info
        self.AAT = dt.fromtimestamp(self.actual_arrival_time['epoch'])
        self.EAT = dt.fromtimestamp(self.estimated_arrival_time['epoch'])
        self.ADT = dt.fromtimestamp(self.actual_departure_time['epoch'])
        self.EDT = dt.fromtimestamp(self.estimated_departure_time['epoch'])
        
        self.origin_code         = self.origin['code']
        self.origin_airport      = self.origin['airport_name']
        self.destination_code    = self.destination['code']
        self.destination_airport = self.destination['airport_name']
    def __repr__(self):
        return self.faFlightID


class FlightRoute:
    def __init__(self, route=dict()):
        self.__dict__ = route
        self.last_departuretime = dt.fromtimestamp(self.last_departuretime)
    def __repr__(self):
        return self.route


class FlightAware(object):
    def __init__(self, username, apikey):
        self.auth     = (username,apikey)
    
    def AirportInfo(self, airport):
        result = readjson('AirportInfo', {'airport_code':airport}, self.auth)
        return FlightResult(result['AirportInfoResult'])

    def AirlineInfo(self, airline):
        result = readjson('AirlineInfo', {'airline_code':airline}, self.auth)
        return FlightResult (result['AirlineInfoResult'])
    
    def FlightInfoStatus(self, ident):
        result = readjson('FlightInfoStatus', {'ident':ident}, self.auth)
        flightresults = result['FlightInfoStatusResult']['flights']
        return [FlightInfo(flight) for flight in flightresults]
    
    def RoutesBetweenAirports (self, origin, destination):
        result = readjson('RoutesBetweenAirports', {'origin':origin, 'destination':destination}, self.auth)
        routeresults = result['RoutesBetweenAirportsResult']['data']
        return [FlightRoute(route) for route in routeresults]
    
    def LatLongsToDistance (self, (lat1,lon1), (lat2,lon2)):
        result = readjson('LatLongsToDistance', {'lat1':lat1, 'lon1':lon1, 'lat2':lat2, 'lon2':lon2}, self.auth)
        self.miles = result['LatLongsToDistanceResult']
        self.km    = self.miles * 1.609344
        return FlightResult({'miles':self.miles, 'km':self.km})
        

