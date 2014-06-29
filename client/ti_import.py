#!/usr/bin/python
from csv import DictReader
from api import PyContactBD
import json
import os
import re
#import gnupg
from keys import key

debug = True


def import_gpg(filename):
    gpg = gnupg.GPG(homedir=os.environ['GNUPGHOME'])
    gpg.ignore_dirty_encoding()
    import_resurl = gpg.import_keys(filename)
    return import_resurl


def dump_import(contactdb, filename):
    reader = DictReader(open(filename), delimiter=';')
    for l in reader:
	# check if we should import it
	status = l['TI Level']
	if status not in ['Listed', 'Accredited', 'Certified']: 
		continue
        phone_number = re.split(' - ', l['Telephone'])[0]
        url = re.split(' - ', l['WWW'])[0]
        # FIXME: we lose the special meaning of the * in the country name
        country = l['Country'].strip('*')
        if country == 'World Wide':
            country = 'WW'
        elif country == 'Europe':
            country = 'EU'
        org = {
            'name': l['Team Name'],
            'long_name': l['Official Team Name'],
            'countrycodes': [country],
            'phone_number': phone_number,
            'emergency_phone': l['Emergency Phone'],
            'fax': l['Telefax'],
            'email': l['Email'],
            # 'business_hh_start': l['-Business Hours'],
            # 'business_hh_end': l['-Business Hours'],
            'pgp_fingerprint': l['PGP Key (Team)'],
            'url': url,
            'ti_url': l['TI URL'],
            'created': l['Date of Establishment'],
            'date_established': l['Date of Establishment'],
            'last_updated': l['Last changed'],
            'source': ['TI'],
            }
        if debug:
            print org
        response = contactdb.post_organisation(json.dumps(org))
        if response.status_code >= 300:
            print response.text

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'

    contactdb = PyContactBD(url, key)
    # import_gpg('../ti/ti-l2-pgpkeys.asc')
    #dump_import(contactdb, '../ti/ti-l2-info.csv')
    dump_import(contactdb, '../ti/ti-l2-l1-l0-info.v2.csv')
