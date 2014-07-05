#!/usr/bin/env python
from csv import DictReader
from api import PyContactBD
import json
import os
import re
import gnupg
from keys import key

debug = False


def import_gpg(filename):
    gpg = gnupg.GPG(homedir=os.environ['GNUPGHOME'])
    gpg.dirty_encoding_ignore()
    import_result = gpg.import_keys(open(filename, 'r').read())
    return import_result


def make_short_id():
    gpg = gnupg.GPG(homedir=os.environ['GNUPGHOME'])
    gpg.dirty_encoding_ignore()
    keys = gpg.list_keys()
    to_return = {}
    for k in keys:
        short_id = k['keyid'][-8:]
        to_return[short_id] = k['fingerprint']
    return to_return


def dump_import(contactdb, filename):
    reader = DictReader(open(filename), delimiter=';')
    pgp_keys_shortids = make_short_id()
    for l in reader:
        # check if we should import it
        status = l['TI Level']
        if status not in ['Listed', 'Accredited', 'Certified']:
            continue
        phone_number = re.split(' - ', l['Telephone'])[0]
        url = re.split(' - ', l['WWW'])[0]
        pattern = re.compile(' - ')
        address = pattern.sub('\n', l['Address'])
        if debug:
            print "XXXXX address: '" + address + "'"
        # FIXME: we lose the special meaning of the * in the country name
        country = l['Country'].strip('*')
        if country == 'World Wide':
            country = 'WW'
        elif country == 'Europe':
            country = 'EU'
        fingerprint = ''
        if status in ['Accredited', 'Certified']:
            if len(l['PGP Key (Team)']) == 0:
                print l['PGP Key (Team)'], 'has no PGP key.'
            else:
                k = l['PGP Key (Team)'][2:]
                fingerprint = pgp_keys_shortids.get(k, '')
                if len(fingerprint) == 0:
                    print l['PGP Key (Team)'], 'not fount in the dump.'
                    print 'Contact', l['Official Team Name']
        org = {
            'name': l['Team Name'],
            'long_name': l['Official Team Name'],
            'countrycodes': [country],
            'address': address,
            'phone_number': phone_number,
            'emergency_phone': l['Emergency Phone'],
            'fax': l['Telefax'],
            'email': l['Email'],
            # 'business_hh_start': l['-Business Hours'],
            # 'business_hh_end': l['-Business Hours'],
            'pgp_fingerprint': fingerprint,
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
#    url = 'http://193.191.172.240:80'

    contactdb = PyContactBD(url, key)
    import_gpg('../ti/ti-l2-pgpkeys.asc')

    dump_import(contactdb, '../ti/ti-l2-l1-l0-info.v2.csv')
