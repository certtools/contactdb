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
        return self.__get('user')

    def get_persons(self):
        return self.__get('person')

    def get_organisations(self):
        return self.__get('organisation')

    def __get(self, model):
        session = self.__prepare_session()
        return session.get('{}/{}s/'.format(self.url, model))

    def get_person_by_name(self, name):
        return self.__get_by_name('person', name)

    def get_org_by_name(self, name):
        return self.__get_by_name('organisation', name)

    def __get_by_name(self, model, name):
        session = self.__prepare_session()
        return session.get('{}/{}s/?name={}'.format(self.url, model, name))

    def get_PGP_Key(self, fingerprint):
        session = self.__prepare_session()
        return session.get('{}/pgpkeys/{}/'.format(self.url, fingerprint))

    def get_asn(self, asn):
        session = self.__prepare_session()
        return session.get('{}/asns/{}/'.format(self.url, asn))

    def post_organisation(self, organisation):
        return self.__post('organisation', organisation)

    def post_person(self, person):
        return self.__post('person', person)

    def post_source(self, source):
        return self.__post('source', source)

    def post_cc(self, cc):
        return self.__post('countrycode', cc)

    def post_asn(self, asn):
        return self.__post('asn', asn)

    def __post(self, model, obj):
        session = self.__prepare_session()
        return session.post('{}/{}s/'.format(self.url, model), obj)

    def update_asn(self, asn):
        return self.__update('asn', asn)

    def update_person(self, person):
        return self.__update('person', person)

    def __update(self, model, obj):
        session = self.__prepare_session()
        if model == 'asn':
            o_id = obj['asn']
        else:
            o_id = obj['id']
        return session.put('{}/{}s/{}/'.format(self.url, model, o_id),
                           json.dumps(obj))
