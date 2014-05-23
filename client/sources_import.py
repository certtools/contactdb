#!/usr/bin/python
from api import PyContactBD
import json
from keys import key

sources = {('TI', 0.9), ('FIRST', 0.9)}


def sources_import(contactdb):
    for source, reliability in sources:
        s = {'name': source, 'reliability': reliability}
        response = contactdb.post_source(json.dumps(s))
        if response.status_code >= 300:
            print response.text

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'

    contactdb = PyContactBD(url, key)

    sources_import(contactdb)
