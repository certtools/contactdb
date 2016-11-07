#!/bin/bash

echo "OpenSSL is going to ask you for the passphrase you used while exporting your cert from the browser."
openssl pkcs12 -in cert.p12 -out ca.pem -cacerts -nokeys
echo "OpenSSL is going to ask you for the passphrase you used while exporting your cert from the browser."
openssl pkcs12 -in cert.p12 -out client.pem -clcerts -nokeys
echo "OpenSSL is going to ask you for the passphrase you used while exporting your cert from the browser."
echo "Then, you will also have to enter, and confirm, a passphrase for the private key in PEM format."
openssl pkcs12 -in cert.p12 -out key.pem -nocerts
