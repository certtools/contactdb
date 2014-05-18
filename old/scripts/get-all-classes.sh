#!/bin/sh

grep class contactdb/models.py | grep -v Meta | perl -n -i -e '/ ([^(]*)\(/ && print "$1\n"; '
