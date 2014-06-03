#!/bin/bash

set -e
set -x

CODENAME=`lsb_release -c | awk '{print $2;}'`
SOURCE="deb http://apt.postgresql.org/pub/repos/apt/ $CODENAME-pgdg main"

sudo bash -c "echo '$SOURCE' >/etc/apt/sources.list.d/pgdg.list"
sudo bash -c 'wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -'

sudo apt-get update
sudo apt-get install postgresql-9.3
sudo apt-get install postgresql-server-dev-9.3
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
sudo sed -i "s/^\(local[ ]*all[ ]*all.*\)peer/\1trust/" /etc/postgresql/9.3/main/pg_hba.conf
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
