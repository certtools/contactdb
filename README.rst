

===========================
How to get the source code
===========================

You can get the source code at 

::

$ git clone git@github.com:ddurvaux/contactdb.git

The private version is available at: 
$ git clone git@git.lo-res.org:/home/git/contactdb.git


If you want to make some changes do it like this:

::

$ git clone git@github.com:ddurvaux/contactdb.git
$ vim README
$ git commit -am 'fix for the README file'
$ git push origin master


In case it does not work, contact aaron@lo-res.org 


==========================
Starting the contactdb 
==========================

# make sure that you can download PGP keys to a keyring

cd <installdirectory>
export CONTACTDB_HOME=$(pwd)
mkdir $CONTACTDB_HOME/.gnupg/ && chmod 700 $CONTACTDB_HOME/.gnupg



