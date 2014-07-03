#!/bin/bash

echo "cURL is going to ask you for the passphrase you used while converting your private key from PKCS#12 to PEM format."
curl -k https://tiw.trusted-introducer.org/directory/ti-l2-pgpkeys.asc --key key.pem --cacert ca.pem --cert client.pem: > ti-l2-pgpkeys.asc
echo "cURL is going to ask you for the passphrase you used while converting your private key from PKCS#12 to PEM format."
curl -k https://tiw.trusted-introducer.org/directory/ti-l2-l1-l0-info.v2.csv --key key.pem --cacert ca.pem --cert client.pem: > ti-l2-l1-l0-info.v2.csv

