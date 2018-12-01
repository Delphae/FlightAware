#!/usr/bin/env python
# coding: utf-8

'''
Looking for Latitude and Longitude for a location
Uses Open Geocoding API - MAPQUEST
https://developer.mapquest.com

'''
import requests
APIKEY = 'NOwxJoFrEFq7z92AZbftbATxhyrOpzBGF'
MAXRESULTS = 10

city = 'Amsterdam'

url = 'http://www.mapquestapi.com/geocoding/v1/address'
params = {'location':city,
          'outFormat':'json',
          'maxResults':MAXRESULTS,
          'key':APIKEY}

response = requests.get(url, params=params)
mapquest = response.json()
results = mapquest['results']

for result in results:
    locations = result['locations']
    for location in locations:
        print ('%4s %12f %12f' % (location['adminArea1'],
                                 location['latLng']['lat'],
                                 location['latLng']['lng']))
