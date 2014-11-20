
=======
About
=======

The ContactDB project was initiated to cover the need for a tool
to maintain contacts for CSIRT teams. The first POC was designed
based on specification of a few CERT team including CERT.at, CIRCL,
CERT.pt and CERT.be.


===========================
(Expected) Features
===========================

* Secure implementation
* Easy and modular web interface
* Integration with 3rd party tools like AbuseHelper
* Support for GPG public key storage
* Delegation (an organisation can keep his contact info up-to-date)
* ...


===========================
How to get the source code
===========================

You can get the source code at

::

  $ git clone git@github.com:certtools/contactdb.git

The private version is available at::

  $ git clone git@git.lo-res.org:/home/git/contactdb.git

Note: the private repo contains importers and data which is not public at the moment.
That's why we have a private repo as well. The source code is the same however.


If you want to make some changes do it like this:

::

  $ git clone git@github.com:certtools/contactdb.git
  $ vim README.rst
  $ git commit -am 'fix for the README file'
  $ git push origin master


In case it does not work, contact aaron@lo-res.org


==========================
Starting the contactdb
==========================

First read the INSTALL.rst file and follow the instructions.

# Here is how to start the contactdb::

  cd <installdirectory>

  export CONTACTDB_HOME=$(pwd)
  mkdir $CONTACTDB_HOME/.gnupg/ && chmod 700 $CONTACTDB_HOME/.gnupg
  echo export CONTACTDB_HOME=$(pwd) >> ./virtenv/bin/activate
  echo export GNUPGHOME=$(pwd)/.gnupg >> ./virtenv/bin/activate

  . ./virtenv/bin/activate
  pip install -r requirements.txt --upgrade

  python ./manage.py syncdb
  python ./manage.py runserver

Then you connect your browser to http://127.0.0.1:8000 and log in.




