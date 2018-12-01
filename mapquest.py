#!/usr/bin/env python
# coding: utf-8

'''
Open Geocoding API - MAPQUEST
https://developer.mapquest.com

'''
import requests
APIKEY = 'MAPQUEST APIKEY'

city = 'Amsterdam'
url = 'http://www.mapquestapi.com/geocoding/v1/address?key=%s&location=%s&outFormat=json&maxResults=1' % (APIKEY, city)

response = requests.get(url)
mapquest = response.json()
results = mapquest['results']
locations = results[0]['locations']

location = locations[0]
print location['latLng']['lat'], location['latLng']['lng']
