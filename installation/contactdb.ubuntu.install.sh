# Contributors:
# "Tomas Lima (CERT.PT)" <tomas.lima@cert.pt>,
# "Mauro Silva (CERT.PT)" <mauro.silva@cert.pt>



echo
echo "=== Warning ==="
echo
echo "Please, execute this script as root"
echo "  # sudo su"
echo "  # sh INSTALL.ubuntu.sh"
echo
echo "If you are executing as root, press ENTER"
echo
read choice


clear
echo "Installing Dependencies [PRESS ENTER]"
echo "====================================="
read choice
apt-get update
apt-get upgrade -y
apt-get install postgresql-9.1 -y
apt-get install python2.7 -y
apt-get install python-setuptools -y
apt-get install python-pip -y
#apt-get install python-django -y
wget https://launchpad.net/ubuntu/+archive/test-rebuild-20130917/+build/5014357/+files/python-django_1.5.3-1_all.deb
dpkg -i python-django_1.5.3-1_all.deb
rm python-django_1.5.3-1_all.deb
apt-get install python-psycopg2 -y
apt-get install python-imaging -y
apt-get install python-ipy -y
apt-get install python-mimeparse -y
pip install django-ipyfield
pip install django-tastypie
pip install python-gnupg
easy_install geopy


sleep 3
clear
echo
echo "Edit the certdir/settings.py file to suite your needs [PRESS ENTER]"
echo "====================================="
echo -n "

--- Change this parameters ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'contactdb',                                          # Or path to database file if using sqlite3.
        'USER': 'contactdb',                                            # Not used with sqlite3.
        'PASSWORD': '',                                                     # Not used with sqlite3.
        'HOST': '',                                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                                         # Set to empty string for default. Not used with sqlite3.
    }
}


--- Add to variable INSTALLED_APPS the following 'tastypie' parameter ---
INSTALLED_APPS = (
    'tastypie',  
        ...
)
"
echo
read choice


clear
echo
echo "Change PostreSQL configuration [PRESS ENTER]"
echo "====================================="
echo "Edit the file: /etc/postgresql/9.1/main/pg_hba.conf
Change this line:
'local   all             all                                     peer'
To:
local   all             all                                     trust"
read choice


clear
echo
echo "Setting up the Database [PRESS ENTER]"
echo "====================================="
read choice
echo "... creating user 'contactdb' ..."
su - postgres -c 'createuser -s contactdb'
echo "... creating database 'contactdb' ..."
su - postgres -c 'createdb contactdb'
echo
echo "... creating database structure ..."
python ./manage.py syncdb


sleep 3
clear
echo
echo "Set your environment variables to use UTF-8 [PRESS ENTER]"
echo "====================================="
read choice
export LANG="en_EN.UTF-8"
export LC_COLLATE="en_EN.UTF-8"
export LC_CTYPE="en_EN.UTF-8"
export LC_MESSAGES="en_EN.UTF-8"
export LC_MONETARY="en_EN.UTF-8"
export LC_NUMERIC="en_EN.UTF-8"
export LC_TIME="en_EN.UTF-8"
export LC_ALL=
export CONTACTDB_HOME=$(pwd)


clear
echo
echo "Fill in the DB values [PRESS ENTER]"
echo "====================================="
read choice
cd ./db/initialize/
sh ./initialize-db.sh
cd ../..


sleep 3
clear
echo
echo "Import the TI csv into the database [PRESS ENTER]"
echo "====================================="
echo -n "Execute: psql -U postgres contactdb <  tidb.csv"
read choice


clear
echo
echo "Start the local Django server [PRESS ENTER]"
echo "====================================="
echo -n "./manage.py runserver"
read choice


clear
echo
echo "Ready! [PRESS ENTER]"
echo "====================================="
echo -n "Connect your browser to http://localhost:8000/admin
        You should see lots of data in the Organisations table"
read choice
