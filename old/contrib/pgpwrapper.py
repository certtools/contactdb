#!/usr/bin/env python

import os
import gnupg
from __future__ import print_function

pgphome=gnupghome=os.environ['CONTACTDB_HOME'] + '/.gnupg/'
gpg = gnupg.GPG(gnupghome=pgphome)
keyserver = 'subkeys.pgp.net'

cipherprefs="""Cipher: AES256, AES192, AES, CAST5, 3DES
            Digest: SHA512, SHA384, SHA256, SHA224, SHA1
            Compression: ZLIB, BZIP2, ZIP, Uncompressed
            Features: MDC, Keyserver no-modify"""

def genkey():
    #keyparams = dict({ 'name_real': 'ContactDB',
    #     'name_email': 'contactdb@contactd.be',
    #     'nname_comment': 'automatically generated, signing only key',
    #     'key_type': 'RSA',
    #     'key_length': 4096,
    #     'key_usage': '',
    #     'subkey_type': 'RSA',
    #     'subkey_length': 4096,
    #     'subkey_usage': 'encrypt,sign,auth',
    #     'passphrase': 'secretSauce' })
    #     #'preferences': cipherprefs, }
    alice = { 'name_real': 'Alice',
        'name_email': 'alice@inter.net',
        'expire_date': '2014-04-01',
        'key_type': 'RSA',
        'key_length': 4096,
        'key_usage': '',
        'subkey_type': 'RSA',
        'subkey_length': 4096,
        'subkey_usage': 'encrypt,sign,auth',
        'passphrase': 'sekrit'}

    print alice

    #keyinput =  gpg.gen_key_input(**keyparams)
    #print keyinput
    key = gpg.gen_key(keyinput)
    assert key is not None
    assert key.fingerprint is not None
    print key
    assert key.fingerprint
    return key

def get_pgpkey(key_id):
    #gpg.search_keys(key_id, keyserver)
    import_result = gpg.recv_keys(keyserver, key_id)
    print import_result



if __name__ == "__main__":
    genkey()
    get_pgpkey('AAAAAAAA')


