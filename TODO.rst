


=============
GENERAL
=============

clean up the mess in scripts/* db/* contrib/* and unify it

=============
Model
=============

* fix m-to-n relationship CERT to country. Some CERTs are responsible for multiple countries. 
* fix m-to-n relationship CERT to URL
* fix 1-n relationship between Organisation and email addresses
* fix 1-n relationship between Organisation and tel#s
* 1-n relationship Person to IM system (Skype, jabber,...)
* parse address correctly (should we split it up?) -> better to get it directly from TI. 
  DONE / decided: we have one address field. This has all the address info in it. We don't try to be smarter in separating the different parts of an address (house number, zip code etc... that's too complex).
* parse all TI fields and fill them into the DB
* geolocate at Organisation INSERT time: use the google API?

PGP
-----
* fix 1-n: multiple addresses per PGP key,   DONE
* fetch unknown PGP keys from the keyserver or the TI keyring
* fix 1-n: multiple keys per person / org

==========
API
==========
* define REST API in a document
* implement best match search algo: given an IP address, ASN, netblock or country code, give me best abuse email contact
* permission system for the RESTful API? How to do it? ACLs or unix-style rwx-rwx-rwx for each path element of the RESTful URL?
* think about who can see what part of the tree / DB? Permission system

* think about federation: how can we make a tree of orgs that are federated? Should we re-use existing directory structures such as DNS?
  should we take some ideas from linkeddata.org ?


==========
Exporters
==========
* Person/user tables export to LDAP 
* -------- " ----------     to VCard
* Test VCard export w. Mac Addressbook
* download picture for person from { internet, ops-t, FB, xing, linked in, ...}
* keyring download



==============
Functionality
==============
* Vouching:
  - document vouching mechanism
  - implement vouching mechanism
* think what ppl need from the contactDB -> social network ---> that's a different app! not in this one ("CERTbook")
* add bio/personal knowledge to contactDB ---> that's a different app! not in this one ("CERTbook")


* write a whois server. output format: like cymru


===============
User Interface
===============

* Build the UI with Django templates with:
  - bootstrap 3
  - typeahead.js
* make google map of all CERTs (c.f. contrib example)
 
===============
Admin Interface
===============

* admin.py: all classes which should be editable should be here
* admin.py: list_fields


=======================================
Supporting / External contact databases
=======================================

List of external data sources:
- TI DB: https://tiw.trusted-introducer.org/directory/index.html
- FIRST DB: www.first.org/members/teams/
- National CSIRT db: https://nationalcsirts.cert.org/
- whois (and especially all kinds of whois abuse searches):
  - Perls' Net::Abuse service
  - ZCW (?): http://www.fr2.cyberabuse.org/whois/?page=downloads
  - RIPE stats JSON interface: https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=AS16010 or 
        https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=<ip>
  - other registries: ARIN etc
  - ENISA Certmap?
  - ... extend... 

Initial DB import
-----------------
* Supporting data:
  - iso country codes: make better initialize.sh script which downloads the ISO codes on it's own
  - patch list of countries: "UK" and "EU"

* INitial basic data should be filled in at installation time:
  - sources table: TI and FIRST
  - list of countries
* geolocate at Organisation INSERT time: use the google API?


TI DB import 
---------------
* multilines are a problem: should we make lots of 1-n relationships out of it (email addr to org) or just have multiline entries? I prefer the latter.

FIRST DB import 
---------------
* look at it

whois proxy / whowas service
---------------------------
It would be great to use the certdir project to also have a whowas service. Idea:
query a whois object and the DB will do that for you as a proxy but also save the result, timestamp it and it can read from the cache if needed


================
Misc.
================

DONE: Why we are using the AH word? This is a contactDB... may be in future will be integrated with AH.
  --> no problem. Let's change the name ->  Rename AHDjango to CERTDir DONE

