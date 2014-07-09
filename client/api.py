#!/usr/bin/python

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

    def get_organisations(self):
        session = self.__prepare_session()
        return session.get(self.url + '/organisations/')

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
