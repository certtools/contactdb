#!/bin/sh


psql -U contactdb contactdb < ./sources.sql 
psql -U contactdb contactdb < ./countries.sql
#psql -U contactdb contactdb < ./internation-airport-sql.output 
