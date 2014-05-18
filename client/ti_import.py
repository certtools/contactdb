#!/usr/bin/python
from csv import DictReader
from api import PyContactBD
import json
from keys import key


def dump_import(contactdb, filename):
    reader = DictReader(open(filename), delimiter=';')
    for l in reader:
        # FIXME: we lose the special meaning of the * in the country name
        country = l['Country'].strip('*')
        if country == 'World Wide':
            country = 'WW'
        if country == 'Europe':
            country = 'EU'
        org = {
            'name': l['Team Name'],
            'fullname': l['Official Team Name'],
            'country': country,
            'phone': [l['Telephone']],
            'emergency_phone': [l['Emergency Phone']],
            'fax': [l['Telefax']],
            'email': [l['Email']],
            'ti_url': l['TI URL'],
            'created': l['Date of Establishment'],
            'website': l['WWW'],
            'date_established': l['Date of Establishment'],
            'last_updated': l['Last changed'],
            }
        response = contactdb.post_organisation(json.dumps(org))
        if response.status_code >= 300:
            print response.text

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'

    contactdb = PyContactBD(url, key)
    dump_import(contactdb, '../ti/ti-l2-info.csv')
