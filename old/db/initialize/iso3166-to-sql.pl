#!/usr/bin/perl

use strict;
use warnings;
use Net::FTP;

# To retrieve the country code file, you could
# use the following command:
# wget ftp://ftp.ripe.net/ripe/hostcount/iso3166-codes
# (DONE AUTOMATICALLY BY THIS SCRIPT)
#
# The information is coming from RIPE and supposed to
# be correct

# delete the code file if it exists
if(-e "./iso3166-codes")
{
    unlink("./iso3166-codes");
}

# download the last version of the file
my $ftp = Net::FTP->new("ftp.ripe.net", Debug => 0)
    or die "Imposssible to connect to RIPE FTP: $@";
$ftp->login("anonymous", "anonymous")
    or die "Login on RIPE FTP failed: ", $ftp->message;
$ftp->cwd("/ripe/hostcount/")
    or die "Impossible to move to ftp://ftp.ripe.net/ripe/hostcount/: ", $ftp->message;
$ftp->get("iso3166-codes")
    or die "Impossible to retrieve ISO3166 file: ", $ftp->message;
$ftp->quit;

# parse the file and procude SQL output
open CODES, "<./iso3166-codes";
open RESULT, ">./iso3166-codes.sql";
while(my $line = <CODES>)
{
    if($line =~ /^(.+)\s+([a-zA-Z]{2})\s+([a-zA-Z]{3})\s+(\d{3})\s*$/)

    {
        my $name  = $1;
        my $code2 = $2;
        my $code3 = $3;

        #trim name
        $name =~ s/\s*$//;

        # @todo - one day, maybe, check what we output here ;)
        print RESULT "INSERT INTO CountryCode (cc, cc3, country_name) VALUES ('$code2', '$code3', '$name');\n";

    }
}
print "INSERT INTO CountryCode (cc, cc3, country_name) VALUES ('UK', 'GBR', 'Great Brittain');\n";

close CODES;
close RESULT;

# That's all folk ;)

