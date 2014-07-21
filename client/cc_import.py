#!/usr/bin/env python

import urllib2
import json

from api import PyContactBD
from keys import key


def dump_import(contactdb, dump):
    for entry in dump:
        cc = {
            'cc': entry['alpha-2'],
            #'cc3': entry['alpha-3'],
            'country_name': entry['name']
            }
        contactdb.post_cc(json.dumps(cc))


def add_custom_TI(contactdb):
    worldwide = {'cc': 'WW', 'cc3': 'WWD', 'country_name': 'World Wide'}
    europe = {'cc': 'EU', 'cc3': 'EUR', 'country_name': 'Europe'}
    uk = {'cc': 'UK', 'cc3': 'GBR', 'country_name': 'United Kingdom'}
    contactdb.post_cc(json.dumps(worldwide))
    contactdb.post_cc(json.dumps(europe))
    contactdb.post_cc(json.dumps(uk))


if __name__ == '__main__':
    source = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json'

    response = urllib2.urlopen(source)
    json_iso3166 = json.loads(response.read())

    url = 'http://127.0.0.1:8000'

    contactdb = PyContactBD(url, key)
    dump_import(contactdb, json_iso3166)
    add_custom_TI(contactdb)
