#!/usr/bin/env python2.7

""" NOTE: this is outdated... """

import csv
import pprint
import sys
import gnupg
import os
import re
import logging

#gpg = gnupg.GPG(gnupghome='/Users/aaron/.gnupg', verbose=True) # os.environ['HOME'])
gpg = gnupg.GPG(verbose=False, use_agent=True) 
#gpg.encoding = 'UTF-8'
#gpg.encoding = 'latin-1'
gpg.encoding = 'latin-1'
public_keys = gpg.list_keys()


def extract_email(str):
    res =  re.search('<([^>]+)>', str, re.I)
    if (None!= res and res.groups):
        return (res.group(1))


def print_insert_stmt(email, key_id):
    try:
        if (email and key_id):
            print "INSERT into contactdb_pgpuid (pgp_email, pgp_key_id) VALUES ('%s', '%s'); " %(email, key_id)
    except:
        logging.warning('could not convert email: ' + email)


for k in public_keys:
    k_id =  "0x" + k['keyid'][8:]
    print "-- %s" %k_id      # just for info
    emails = list(set(map(extract_email, k['uids']) ))
    #print emails
    for e in emails:
        print_insert_stmt(e, k_id)

    #for e in emails:
        #e = unicode(e, 'utf-16')
    #    print "%s" %e
    #    print "INSERT into contactdb_pgpuid (email, pgp_key_id) VALUES ('%s', '%s')" %(e, k_id)

    

exit (0)


csvDictReader = csv.DictReader(open(sys.argv[1], 'rb'), restkey='rest', dialect='excel') #, delimiter=',', quotechar='"')

for row in csvDictReader:
    k_id = row['PGP Key (Team)']
    print """INSERT INTO contactdb_pgpkey ( pgp_key_id, pgp_key, pgp_key_email, pgp_key_created, pgp_key_expires )
VALUES ( '%s', '%s', '%s', '%s', '%s' );
""" %( k_id, key(k_id), email(k_id), created(k_id), expires(k_id) )

