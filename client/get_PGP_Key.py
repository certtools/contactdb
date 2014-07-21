#!/usr/bin/env python

from api import PyContactBD
from keys import key

fp = 'CA572205C0024E06BA70BE89EAADCFFC22BD4CD5'


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
    contactdb = PyContactBD(url, key)

    r = contactdb.get_PGP_Key(fp)
    print r.json()[fp]
