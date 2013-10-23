#!/usr/bin/perl

use strict;
use warnings;

# To retrieve the country code file, you could
# use the following command:
# wget ftp://ftp.ripe.net/ripe/hostcount/iso3166-codes
#
# The information is coming from RIPE and supposed to
# be correct

# In and output files
open CODES, "<./iso3166-codes";
open CODESSQL, ">./iso3166-sql.output";
open AIRPORTS, "<./international-airport.txt";
open AIRPORTSSQL, ">./internation-airport-sql.output";

# Internal state
my %countries2cc;

# Parse all the ISO3166 codes
while(my $line = <CODES>)
{
    if($line =~ /^(.+)\s+([a-zA-Z]{2})\s+([a-zA-Z]{3})\s+(\d{3})\s*$/)
    {
        my $name  = $1;
        my $code2 = $2;
        my $code3 = $3;

        #trim name
        $name =~ s/\s*$//;

        # TODO ADD SUPPORT FOR CHAR ' in country name
        
        print CODESSQL "INSERT INTO CountryCode (cc, country_name) VALUES ('$code2', '$name');\n";
        $countries2cc{lc($name)} = $code2;
    }
    else
    {
        print "COUNTRY PARSING ERROR: '$line'\n";
    }
}
close CODES;
close CODESSQL;

# Parse all the airport codes
while(my $line = <AIRPORTS>)
{
    if($line =~ /^(.+),\s+(.+)\s+\(([a-zA-Z]{3})\)$/)
    {
        my $city = $1;
        my $country = $2;
        my $airport = $3;
        
        # if country is mixed up with other info, drop them
        if($country =~ /(.+)\s+\-\s+(.+)/)
        {
            $country = $1;
        }
        
        my $cc2 = $countries2cc{lc($country)}; #TODO: error handling
        if(defined($cc2))
        {
            print AIRPORTSSQL "INSERT INTO AirportCode (code, name, country) VALUES ( '$airport', '$city', '$cc2' );\n";
        }
        else
        {
            print "COUNTRY CODE ERROR: $country\n";
        }
    }
    else
    {
        print "AIRPORT PARSING ERROR: '$line'\n";
    }
} 
close AIRPORTS;
close AIRPORTSSQL;


