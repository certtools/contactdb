#!/usr/bin/env python

import json
import requests


class PyContactBD(object):
    """
        Python API for ContactDB
    """

    def __init__(self, url, key):
        self.url = url
        self.key = key

    def __prepare_session(self):
        """
            Prepare the headers of the session
        """
        session = requests.Session()
        session.headers.update(
            {'Authorization': ' Token ' + self.key,
             'Accept': 'application/json',
             'Content-Type': 'application/json'})
        return session

    def get_users(self):
        session = self.__prepare_session()
        return session.get(self.url + '/users/')

    def get_user_by_name(self, name):
        session = self.__prepare_session()
        return session.get('{}/persons?name={}'.format(self.url, name))

    def get_org_id_by_name(self, name):
        session = self.__prepare_session()
        return session.get('{}/organisations/?name={}'.format(self.url, name))

    def get_organisations(self):
        session = self.__prepare_session()
        return session.get(self.url + '/organisations/')

    def get_PGP_Key(self, fingerprint):
        session = self.__prepare_session()
        return session.get(self.url + '/pgpkeys/' + fingerprint)

    def post_organisation(self, organisation):
        session = self.__prepare_session()
        return session.post(self.url + '/organisations/', organisation)

    def post_person(self, person):
        session = self.__prepare_session()
        return session.post(self.url + '/persons/', person)

    def post_source(self, source):
        session = self.__prepare_session()
        return session.post(self.url + '/sources/', source)

    def post_cc(self, cc):
        session = self.__prepare_session()
        return session.post(self.url + '/countrycodes/', cc)

    def post_asn(self, asn):
        session = self.__prepare_session()
        return session.post(self.url + '/asns/', asn)

    def get_asn(self, asn):
        session = self.__prepare_session()
        response = session.get('{}/asns/{}/'.format(self.url, asn))
        return response.json()

    def update_asn_owners(self, asn_id, owners):
        session = self.__prepare_session()
        asn = self.get_asn(asn_id)
        [asn['owners'].append(o) for o in owners if o not in asn['owners']]
        return session.put('{}/asns/{}/'.format(self.url, asn_id), json.dumps(asn))

#    def update_affiliations(self, )
