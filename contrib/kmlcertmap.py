#!/usr/bin/python

"""
This script parses a CSC file as input and geocode the 'Address' field.
Each entry is then place on a KML file or output as a JSON object.

In json mode, callback function is setCerts()

Usage: kmlcertmap.py CSVFILE OUTPUT [json]


Author: romain.bourgue@gmail.com
"""

import re
import json
import simplekml
import time
import csv
import sys
from geopy import geocoders

nowhere=[(-35.537113,46.316584)]
kml=simplekml.Kml()
def geocode(location,geoQuality=100):
   print("Geocoding"+location+"...")
   try:
      place, (lat, lng)= geocoders.GoogleV3().geocode(location.encode("utf-8"),exactly_one=False)[0]
   except geocoders.googlev3.GTooManyQueriesError:
      print('Too many requests, sleeping a bit')
      time.sleep(0.3)
      return geocode(location,geoQuality)
      
   except geocoders.googlev3.GQueryError:
      
      print("Error couldn't geocode %s" % location)
      if location.count('-')==0:
          print "ERROR Returning Nowhere" 
          return nowhere
      print("Removing first info")
      geoQuality=geoQuality-10
      return geocode('-'.join(location.split('-')[1::]),geoQuality)
      
      
   return [(lng,lat)],geoQuality

class Cert:
   def jsonable(self):
      return self.__dict__
   pass

def addToKML(cert):
    
   pnt=kml.newpoint(name=cert.title, description=cert.description, coords=cert.coords)
   pnt.timespan.begin = cert.date
   #pnt.style.iconstyle.icon.href=job.icon


def parseRow(row):
    cert=Cert()
    cert.geoQuality=100
    if row["Address"]=='. - ':
        print "no address for %s, using country %s" % (row["Official Team Name"],row["Country"])
        row["Address"]=row["Country"]
        cert.geoQuality=10
    
    cert.coords,cert.geoQuality=geocode(row["Address"],cert.geoQuality)
    print "Geoquality is "+str(cert.geoQuality)
    cert.x=cert.coords[0][0]
    cert.y=cert.coords[0][1]
    
    cert.date=row.pop("First entered")
    
    
    cert.title=row.pop("Team Name")
    cert.description=""
    for key in row:
        if row[key]!="":
            
            if re.match("https?://",row[key]):
                cert.description+="- <b>%s</b>: <a href='%s' target=_blank>%s</a><br>" % (key,row[key],row[key])
            elif re.match("@",row[key]):
                cert.description+="- <b>%s</b>: <a href='mailto:%s'>%s</a><br>" % (key,row[key],row[key])
            else:
                cert.description+="- <b>%s</b>: %s<br>" % (key,row[key])
            setattr(cert,re.sub(' ','_',key),row[key])
    
    return cert

certs = []

#Internet Addresses;Email (Rep);Official Team Name;Telefax;Former Team Names;Email;Operating Status;Emergency Phone;TI Level;First entered;Address;PGP Key (T
#eam);Date of Establishment;Last changed;FTP;PGP Key (Rep);Team Representative;Country;Contacting outside Business Hours;Other communication;-Type of Constituency;Country o
# Constituents;Team Name;-Business Hours;WWW;Telephone;*RFC2350;TI URL;FIRST Membership

if len(sys.argv) == 1:
    print "Usage: %s CSVinputfile output [json]" % sys.argv[0]
    exit(0)

csvDictReader = csv.DictReader(open(sys.argv[1], 'rb'), restkey='rest', dialect='excel', delimiter=';', quotechar='"')  

for row in csvDictReader:
    
    if ((row["TI Level"]=="Outdated") or (row["TI Level"]=="Not Operational")):
        print "Skiping outdated info...."
        continue
    cert=parseRow(row)
    
    addToKML(cert);
    certs.append(cert.__dict__)
    
if (len(sys.argv)>3) and (sys.argv[3]=="json"):
    text_file = open(sys.argv[2], "w")
    text_file.write('setCerts('+ json.dumps(certs) +");")
    text_file.close()
else:
    kml.save("/var/www/jobmap/jobmap.kml")
    print("KML document saved")
