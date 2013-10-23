BASEDIR=$(dirname $0)

echo "Droping database.... [PRESS ENTER]"
read
echo "DROP DATABASE contactdb" | psql -U contactdb -d postgres

echo "Recreating database and tables.... [PRESS ENTER]"
read
echo "CREATE DATABASE contactdb" | psql -U contactdb -d postgres
python $BASEDIR/../manage.py syncdb

echo "Importing country codes.... [PRESS ENTER]"
read
psql -U contactdb contactdb < $BASEDIR/../db/initialize/countries.sql

echo "Adding TI as a source.... [PRESS ENTER]"
read
psql -U contactdb contactdb < $BASEDIR/../db/initialize/sources.sql

echo "Import TI data.... [PRESS ENTER]"
read
$BASEDIR/../contrib/TI-import.py <$BASEDIR/../contrib/TI-dump.20130918.csv >foo.sql
psql -U contactdb contactdb < foo.sql
rm foo.sql
