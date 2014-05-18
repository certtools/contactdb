# geolocation module
# Thanks to romain.bourgue@gmail.com


import json
import sys
from geopy import geocoders

# returning latitude and longitude coordinates to a given address using Google API
# @version 1.0 20131209
# @param location - text, specifies the address
# @param geoQuality - specifies the quality of the returning lat/long coordinats. starting at 100% as default
# @param coordinatesOnly - true by default, returns only coordinates, if 0: returning all information (place, latitude + longitude, quality)
# @return latitude and longitude coordinates, optional quality of geolocation and place if specified
def geocode(location,coordinatesOnly=1,geoQuality=100):
   try:
      place, (lat, lng)= geocoders.GoogleV3().geocode(location.encode("utf-8"))

   except geocoders.google.GQueryError:
      print("Error couldn't geocode %s" % location)
      if location.count('-')==0:
          print "ERROR Returning Nowhere"
          return nowhere
      print("Removing first info")
      geoQuality=geoQuality-10
      return geocode('-'.join(location.split('-')[1::]),geoQuality)
   if coordinatesOnly == 1:
   	return (lat,lng)
   else:
	return place,[(lat,lng)],geoQuality

# usage example
# geocode("1010 Vienna", 100)
print(geocode("vienna"))

