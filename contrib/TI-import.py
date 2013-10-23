#!/usr/bin/env python2.7

import sys
import csv
import pprint
import re
import gnupg
import os

gpg = gnupg.GPG(gnupghome=os.environ['CONTACTDB_HOME'] + '/.gnupg/')


#def get_pgpkey(key_id):
#    

def extract_workinghours(field):
    # input format:
    #   09:00 to 17:00 Monday to Friday except public holidays.
    #   Timezone: GMT+01.
    #   Timezone with DST: GMT+02
    match = re.search('.*([0-9]{2}:[0-9]{2}).*(to|\-).*([0-9]{2}:[0-9]{2}).*Timezone: ([^\.]+)', field, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    if (match == None):
        begin_hh = ''
        end_hh = ''
        tz = ''
    else:
        begin_hh = match.group(1)
        end_hh= match.group(3)
        tz = match.group(4)
    return (begin_hh, end_hh, tz)


# new TI format: (number indicates field number)
# 0        1        2             3            4                5      6                  7                 8        9
#Team Name,TI Level,First entered,Last changed,FIRST Membership,TI URL,Official Team Name,Former Team Names,Country,
# 9                    10                    11                12                   13               14
#Date of Establishment,-Type of Constituency,Constituency ASNs,Constituency Domains,Costituency Nets,Country of Constituents,
# 15   16             17        18              19      20                  21
#Email,PGP Key (Team),Telephone,Emergency Phone,Telefax,Other communication,Address,
# 22             23                                24                  25
#-Business Hours,Contacting outside Business Hours,Team Representative,Email (Rep),
# 26           27  28   29      30
#PGP Key (Rep),WWW,FTP,*RFC2350,Operating Status
#


#ACOnet-CERT,Accredited,8/31/00,3/28/03,Full Member,https://tiw.trusted-introducer.org/directory/teams/aconet-cert.html,ACOnet-CERT,,AT,1/1/03,Research & Education,AS1853. - AS679. - AS760. - AS1109-AS1123. - AS1205. - AS1776. - AS1921. - AS2036. - AS2494. - AS2604. - AS6720. - AS8692. - AS12991. - AS16314. - AS30971. - AS39837. - AS41915. - AS42685. - AS47515,ac.at,,AT,cert@aco.net,0x86EDDB8A,+43 1 427714045,+43 1 427714045,+43 1 42779140,N/A,Zentraler Informatikdienst. - Universitaet Wien. - Universitaetsstrasse 7. - A-1010 Wien. - Austria,09:00 to 17:00 Monday to Friday except public holidays. - Timezone: GMT+01. - Timezone with DST: GMT+02,eMail or leave Message on the Voicebox,Alexander Talos-Zens,alexander.talos-zens@univie.ac.at,0x9D9731C5,http://cert.aco.net/,,,

reader = csv.reader(sys.stdin,  delimiter=',')
headers = reader.next()
for r in reader:
    r = [ x.replace( " - ", "\n") for x in r ]
    (begin_hh, end_hh, tz) = extract_workinghours(r[22])
    mapping = { "name": r[0], "fullname": r[6], 
               "address":r[21],
               "country_id":r[8], "phone":r[17], "emergency_phone":r[18],
               "fax":r[19], "email":r[15], "website":r[27], "timezone":tz,  ## XXX FIXME: timezone parsing from field r[22]
               "business_hh_start": begin_hh, "business_hh_end": end_hh,        ## XXX FIXME: parse and split this field r[22]
               "date_established": r[9] ,
               "isCERT": "t",
               "ti_url": r[5],
               "pgp_key_id": r[16],
               "confirmed": "t",
               "active": "t",
               "source_id": "TI",
               }
    #pprint.pprint(mapping)
    # do the mapping
    keystr=""
    valstr=""
    for key in mapping.keys():
        keystr += key + ", "
        valstr += "" + ( 'E' + repr(mapping[key]) if (mapping[key] != '') else 'NULL' ) + ", "
    keystr += 'parent_id'
    valstr += 'NULL'

    # order: 
    # first insert the pgp key and uids if it does not exist yet
    # then the person
    # then the organisation
    print "INSERT INTO contactdb_pgpkey (pgp_key_id) values ( " + repr(r[16]) + " );"
    print "INSERT INTO contactdb_organisation( " + keystr + ") values (" + valstr + ");"

    # now insert all countries (if they don't exist yet) into contactdb_organisation_country

# database format:
# contactdb=# \d contactdb_organisation
#Column          | Type           | Modifiers                              
#-------------------------+--------------------------+---------------------------------------------------------------------
#id                      | integer                  | not null default nextval('contactdb_organisation_id_seq'::regclass)
#parent_id               | integer                  | 
#name                    | character varying(1000)  | not null
#fullname                | character varying(1000) |
#nesting | character varying(5000)  | 
#protection_profile | character varying(30)    | 
#isCERT  | boolean 
#address | character varying(1000)  | 
#housenr | character varying(50)    | 
#pobox | character varying(50)    | 
#city | character varying(200)   | 
#zipcode | character varying(20)    | 
#country_id | character varying(2)     | not null 
#phone | character varying(64) | not null 
#emergency_phone | character varying(64) | 
#fax | character varying(64) | 
#email | character varying(256) | not null 
#website | character varying(1000) | 
#timezone | character varying(10) | 
#business_hh_start | time without time zone | not null
#business_hh_end | time without time zone   | not null
#date_established | date | 
#pgp_key_id | character varying(1000) | 
#confirmed | boolean | not null
#active | boolean | not null
#source_id | character varying(1000) | 
#vouching_proposed_by_id | integer | not null
#ti_url | character varying(1000) | 
#first_url | character varying(1000) | 
#created | timestamp with time zone | not null
#last_updated | timestamp with time zone | not null

