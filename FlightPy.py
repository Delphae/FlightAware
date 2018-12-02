#!/usr/bin/env python
# coding: utf-8

'''
    ____       _       _
   |  _ \  ___| |_ __ | |__   __ _  ___
   | | | |/ _ \ | '_ \| '_ \ / _` |/ _ \
   | |_| |  __/ | |_) | | | | (_| |  __/
   |____/ \___|_| .__/|_| |_|\__,_|\___|
                |_|

1.1  2018-11-30   initial version
1.2  2018-12-01   AirportBoards
1.3  2018-12-02   validate username & apikey
                  WeatherConditions
1.4               TailOwner


'''

VERSION = '1.4'
DATE    = '2018-12-02'

import requests, json
from datetime import datetime as dt


def readjson(method, params, auth):
    url = "https://flightxml.flightaware.com/json/FlightXML3/"
    response = requests.get(url+method, params=params, auth=auth)
#    print response.url
#    print response.status_code
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
    
    def __str__(self):
        try:
            origincity = self.origin['city']
            destincity = self.destination['city']
            return '%-3s %-5s %5s %-25s %5s %s' % (self.airline_iata,
                                       self.flightnumber,
                                       str(self.ADT.time())[:-3],
                                       origincity.encode('iso-8859-1'),
                                       str(self.AAT.time())[:-3],
                                       destincity.encode('iso-8859-1'))
        except:
            return ''


class FlightRoute:
    def __init__(self, route=dict()):
        self.__dict__ = route
        self.last_departuretime = dt.fromtimestamp(self.last_departuretime)
    def __repr__(self):
        return self.route


class FlightAware(object):
    __version__ = VERSION
    __date__    = DATE

    def __init__(self, username='', apikey=''):
        if not username or not apikey:
             conf = json.load(open('flightaware.json'))
             username = conf['username']
             apikey   = conf['apikey']
        self.auth = (username,apikey)
        
        url = "https://flightxml.flightaware.com/json/FlightXML3/WeatherConditions"
        params = {'airport_code':'AMS'}
        response = requests.get(url, params=params, auth=self.auth)
        print ('%s %s' % (response.status_code, response.reason))
    
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
        
    def AirportBoards(self, airport):      
        result = readjson('AirportBoards', {'airport_code':airport}, self.auth)
        boards = result['AirportBoardsResult']
        arrivals   = [FlightInfo(flight) for flight in boards['arrivals']['flights']]
        departures = [FlightInfo(flight) for flight in boards['departures']['flights']]
        enroute    = [FlightInfo(flight) for flight in boards['enroute']['flights']]
        scheduled  = [FlightInfo(flight) for flight in boards['scheduled']['flights']]
        resultdict = dict(arrivals=arrivals,
                          departures=departures,
                          enroute=enroute,
                          scheduled=scheduled)
        return FlightResult(resultdict)
    
    def WeatherConditions(self, airport):
        result = readjson('WeatherConditions', {'airport_code':airport}, self.auth)
        conditionsresult = result['WeatherConditionsResult']['conditions']
        return [FlightResult(condition) for condition in conditionsresult ]

    def TailOwner(self, ident): 
        result = readjson('TailOwner', {'ident':ident}, self.auth)
        return FlightResult(result['TailOwnerResult'])
