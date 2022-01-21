# ARCHIVED PROJECT!

**This project is archived. Development focus moved to other, similar projects such as [tuency](https://gitlab.com/intevation/tuency/tuency). Also have a look at [contacts.cert.at](https://github.com/aaronkaplan/contacts.cert.at) which does a nice mapping between IP 2 country code -> national CERT lookup.**

# Contact DB

## Database Setup

The following commands assume that PostgreSQL is running and listening on the
default port. They create a database called "contactdb" which matches the
default configuration of the bot.

```
    su - postgres

    createdb --encoding=UTF8 --template=template0 contactdb
    psql -f db/initdb.sql   contactdb
    psql -f db/defaults.sql contactdb
```

A database user with the right to select the data in the Contact DB
must be created.  This is the account, which will be used in the bot's
configuration for accessing the database.

```
    createuser contactdbuser --pwprompt
    psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO contactdbuser;" contactdb

```

## Adding New Contacts

This contactDB allows you to either add contacts manually or via so called "shadow tables".
A shadow table is basically a table which contains the same fields as the main table. However, 
the data there is inserted automatically and may be dropped again at will.
A shadow table can be used for lookups (e.g. do we have any contact for network xyz). If nothing is found, the main tables are searched.

The most prominent use of shadow tables is to import the RIPE database (abuse_c contacts from the RIPE DB).

### Manual contacts


Contacts can be added to the database directly using SQL.  These
manually configured contacts will take precedence over contacts which
were imported automatically, i.e. by `ripe_import.py`.

Connect to the database:

```
  su - postgres
  psql contactdb

```
Add a contact:

```pgsql

-- 1. Prepare contact information

  \set asn 3320
  -- unique name of the organization:
  \set org_name 'org1'
  \set org_comment 'Example comment on organization.'
  \set contact_email 'test@example.com'
  \set contact_comment 'Test comment on contact.'
  -- set the notification interval in seconds
  -- an interval of -1 means no notifications will be generated
  \set notification_interval 0

-- 2. Add new contact

  BEGIN TRANSACTION;
  INSERT INTO autonomous_system (number) VALUES (:asn);
  WITH new_org AS (
    INSERT INTO organisation (name,comment)
    VALUES (:'org_name',:'org_comment')
    RETURNING id
  ),
  new_contact AS (
    INSERT INTO contact (email,format_id,comment)
    VALUES (:'contact_email', 2, :'contact_comment')
    RETURNING id
  ),
  new_ota AS (
    INSERT INTO organisation_to_asn (organisation_id,asn_id,notification_interval)
    VALUES (
      (SELECT id from new_org), :asn, :notification_interval
    )
  )
  INSERT INTO role (organisation_id,contact_id) VALUES (
      (SELECT id from new_org),
      (SELECT id from new_contact)
    )
  ;
  COMMIT TRANSACTION;

```

### RIPE database (shadow tables)

Please see the [README](db/README-ripe-import.md) in the db/ directory.



# Generating a graphic which visualizes the schema of the ContactDB

You can use `postgresql-autodoc` to do this. PG autodoc is available on both
debian and ubuntu via apt.
