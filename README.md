
## FlightPy - a Python wrapper for the FlightAware API
#### FlightAware XML v3
The FlightAware API requires not only a valid username, but also a valid API key.

You can request an API key at https://flightaware.com/commercial/flightxml/key
#### Documentation
version 2.0
https://flightaware.com/commercial/flightxml/documentation2.rvt
    
version 3.0 (beta)
https://flightaware.com/commercial/flightxml/v3/documentation.rvt

#### Define an instance of FlightAware with your username and api key


```python
USERNAME = 'YOUR USERNAME'
APIKEY   = 'YOUR API KEY'

from FlightPy import FlightAware

FA = FlightAware(USERNAME,APIKEY)
```

The current version of FlightPy returns FlightAware information with:
<nl>
    <li>method AirportInfo</li>
    <li>method AirlineInfo</li>
    <li>method FlightInfoStatus</li>
    <li>method LatLongsToDistance</li>
    <li>method RoutesBetweenAirports</li>
    <li>method AirportBoards</li>
</nl>

Please read FlightPy_Examples.ipynb with useful examples.

This list will be extended every month with new features. If you would like to callaborate, please do.


