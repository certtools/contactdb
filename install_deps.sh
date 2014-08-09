#!/bin/bash

set -e
set -x

# Debian Wheezy has 9.1
#POSTGRES_VERSION="9.1"

# Ubuntu 14.04 has 9.3
POSTGRES_VERSION="9.3"

sudo apt-get update
sudo apt-get install postgresql-${POSTGRES_VERSION}
sudo apt-get install postgresql-server-dev-${POSTGRES_VERSION}
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
sudo sed -i "s/^\(local[ ]*all[ ]*all.*\)peer/\1trust/" /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf
sudo service postgresql restart

sudo su - postgres -c 'createuser -s contactdb'
#sudo su - postgres -c 'dropdb contactdb'
sudo su - postgres -c 'createdb contactdb'

virtualenv virtenv

echo export CONTACTDB_HOME=$(pwd) >> ./virtenv/bin/activate
echo export GNUPGHOME=$(pwd)/.gnupg >> ./virtenv/bin/activate

. ./virtenv/bin/activate
pip install -r requirements.txt --upgrade

python ./manage.py syncdb
