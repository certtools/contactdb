#!/bin/bash

set -e
set -x

sudo apt-get install postgresql-9.3
sudo apt-get install postgresql-server-dev-9.3
sudo sed -i "s/^\(local[ ]*all[ ]*all.*\)peer/\1trust/" /etc/postgresql/9.3/main/pg_hba.conf
sudo service postgresql restart

sudo su - postgres -c 'createuser -s contactdb'
sudo su - postgres -c 'createdb contactdb'

virtualenv virtenv

echo export CONTACTDB_HOME=$(pwd) >> ./virtenv/bin/activate

. ./virtenv/bin/activate
pip install -r requirements.txt --upgrade

python ./manage.py syncdb
