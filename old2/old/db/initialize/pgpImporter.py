#!/usr/bin/env python2.7

import pprint
import gnupg
import re
import logging
import psycopg2
from psycopg2 import errorcodes


# need to call init() to initialize this
gpgdict = dict()

# ----------------------------------------------------
# functions

def insert_pgp_key(k, dbcursor):
    if (k == None or k == ""):
        print "skipping empty key '%s'" %k
        return

    # first try inserting the key
    try:
        print "inserting pgp key %s"  %k
        #print row
        #print dbcursor.mogrify("INSERT INTO contactdb_pgpkey (pgp_key_id) VALUES (%s)", (k,))
        dbcursor.execute("INSERT INTO contactdb_pgpkey (pgp_key_id) VALUES (%s)", (k,))
        #print "inserted id %d" %(dbcursor.lastrowid)
    except Exception, e:
        print "could not insert pgp key %s"  %k
        print errorcodes.lookup(e)
    # next try to  insert email addresses for that key into the contactdb_pgpuid
    # table
    # fetch emails for this key id
    print "searching for key %s in gpgdict"  %k
    if (k in gpgdict):
        #print "k in gpgdict"
        # found it, insert into contactdb_pgpuid
        for e in gpgdict[k]:
            if (e != None and e != ""):
                #print dbcursor.mogrify("INSERT INTO contactdb_pgpuid (pgp_key_id, pgp_email) VALUES (%s, %s)", (k, e))
                dbcursor.execute("INSERT INTO contactdb_pgpuid (pgp_key_id, pgp_email) VALUES (%s, %s)", (k, e))
    else:
        print "could not find pgp key %s in keyring" %(k)

    return


def extract_email(str):
    res =  re.search('<([^>]+)>', str, re.I)
    if (None!= res and res.groups):
        return (res.group(1))



def init():
    gpg = gnupg.GPG(verbose=False, use_agent=True) 
    #gpg.encoding = 'UTF-8'
    gpg.encoding = 'latin-1'
    public_keys = gpg.list_keys()
    # read in all the keys, now make a dict (key_id -> [ emails,...]
    for k in public_keys:
        k_id =  "0x" + k['keyid'][8:]
        print "-- %s" %k_id      # just for info
        emails = list(set(map(extract_email, k['uids']) ))
        gpgdict[k_id] = emails
    #print gpgdict



def print_insert_stmt(email, key_id):
    try:
        if (email and key_id):
            print "INSERT into contactdb_pgpuid (pgp_email, pgp_key_id) VALUES ('%s', '%s'); " %(email, key_id)
    except:
        logging.warning('could not convert email: ' + email)


    
