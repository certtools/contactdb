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


def get_fingerprint(dict_shortid, shortid):
    if shortid.startswith('0x'):
        shortid = shortid[2:]
    return dict_shortid.get(shortid, '')


def team_import(l, country, status, pgp_keys_shortids):
    phone_number = re.split(' - ', l['Telephone'])[0]
    url = re.split(' - ', l['WWW'])[0]
    if len(url) > 0 and not url.startswith('http'):
        url = 'http://' + url
    pattern = re.compile(' - ')
    address = pattern.sub('\n', l['Address'])
    if debug:
        print "XXXXX address: '" + address + "'"
    fingerprint = ''
    if status in ['Accredited', 'Certified']:
        if len(l['PGP Key (Team)']) == 0:
            print l['Team Name'], 'has no PGP key.'
        else:
            fingerprint = get_fingerprint(pgp_keys_shortids, l['PGP Key (Team)'])
            if len(fingerprint) == 0:
                print 'Key not found', l['PGP Key (Team)'], l['Official Team Name']
    org = {
        'name': l['Team Name'].strip(),
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
        print org


def asn_import(l):
    asns_dirty = re.split('. - ', l['Constituency ASNs'])
    asns = []
    for asn in asns_dirty:
        if asn.upper().startswith('AS'):
            asns.append(asn[2:])
        else:
            asns.append(asn)
    org = contactdb.get_org_by_name(l['Team Name']).json()
    for a in asns:
        asn = {
            'active': True,
            'source': 'TI',
            'owners': [org[0]['id']],
            'asn': a
            }
        j_asn = json.dumps(asn)
        response = contactdb.post_asn(j_asn)
        if response.status_code == 400:
            asn = contactdb.get_asn(a).json()
            if org[0]['id'] not in asn['owners']:
                asn['owners'].append(org[0]['id'])
            response = contactdb.update_asn(asn)
        if response.status_code >= 300:
            print response.text
            print asn


def rep_import(l, country, status, pgp_keys_shortids):
    fingerprint = ''
    if status in ['Accredited', 'Certified']:
        if len(l['PGP Key (Rep)']) == 0:
            print l['Team Representative'], 'has no PGP key.'
        else:
            fingerprint = get_fingerprint(pgp_keys_shortids, l['PGP Key (Rep)'])
            if len(fingerprint) == 0:
                print 'Key not found', l['PGP Key (Rep)'], l['Team Representative']
    org = contactdb.get_org_by_name(l['Team Name']).json()
    existing_persons = contactdb.get_person_by_name(l['Team Representative']).json()
    is_new = True
    has_changed = False
    person = None
    if len(existing_persons) >= 0:
        for p in existing_persons:
            if p['pgp_fingerprint'] == fingerprint:
                # same person
                is_new = False
                if country not in p['countrycodes']:
                    p['countrycodes'].append(country)
                    has_changed = True
                if org[0]['id'] not in p['organisations']:
                    p['organisations'].append(org[0]['id'])
                    has_changed = True
                person = p
                break
    if is_new:
        person = {
            # name as primary key for person: issue with duplicated name
            'name': l['Team Representative'],
            'source': ['TI'],
            'email': l['Email (Rep)'],
            'pgp_fingerprint': fingerprint,
            'countrycodes': [country],
            'organisations': [org[0]['id']]
            }
        response = contactdb.post_person(json.dumps(person))
    elif has_changed:
        response = contactdb.update_person(json.dumps(person))
    if response.status_code >= 300:
        print response.text
        print person


def dump_import(contactdb, filename):
    reader = DictReader(open(filename), delimiter=';')
    pgp_keys_shortids = make_short_id()
    for l in reader:
        # check if we should import it
        status = l['TI Level']
        if status not in ['Listed', 'Accredited', 'Certified']:
            continue
        # FIXME: we lose the special meaning of the * in the country name
        country = l['Country'].strip('*')
        if country == 'World Wide':
            country = 'WW'
        elif country == 'Europe':
            country = 'EU'
        team_import(l, country, status, pgp_keys_shortids)
        if len(l['Constituency ASNs']) > 0:
            asn_import(l)
        if len(l['Team Representative']) > 0:
            rep_import(l, country, status, pgp_keys_shortids)

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
#    url = 'http://193.191.172.240:80'

    contactdb = PyContactBD(url, key)
    import_gpg('../ti/ti-l2-pgpkeys.asc')

    dump_import(contactdb, '../ti/ti-l2-l1-l0-info.v2.csv')
