# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import django.core.validators

validate_url = django.core.validators.URLValidator()
validate_email = django.core.validators.validate_email

import datetime

from contactdb.fields import JSONField
from contactdb.forms.fields import JSONListToNewlineField
from contactdb.forms.widgets import JSONListToNewlineWidget

# Create your models here.

MEDIA_ROOT = '/var/www/upload/'
MEDIA_URL = "/upload/"

class Countrycode(models.Model):
    # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    # we can load this automatically from ripe.NET
    cc = models.CharField(max_length=2, primary_key=True)
    cc3 = models.CharField(max_length=3, null=True, blank=True)
    country_name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.country_name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"



class PGPKey(models.Model):
    pgp_key_id  = models.CharField(max_length=1000, primary_key=True)
    pgp_key = models.TextField(blank=True,null=True)
    pgp_key_created = models.DateTimeField("Created", null=True, blank=True)
    pgp_key_expires = models.DateTimeField("Expires", null=True, blank=True)

    def __unicode__(self):
        #return self.pgp_key_id + '(' + self.pgp_key_email + ')'
        return self.pgp_key_id 

    class Meta:
        verbose_name = "PGP Key"


class PGPUid(models.Model):
    pgp_email = models.EmailField(verbose_name="Email (UID)")
    pgp_key = models.ForeignKey(PGPKey)

    def __unicode__(self):
        return self.pgp_key.pgp_key_id + " <" + self.pgp_email + ">"

    class Meta:
        verbose_name = "PGP UID"
        verbose_name_plural = "PGP UIDs"


class Source(models.Model):
    name = models.CharField(max_length=1000, primary_key=True)
    reliability = models.FloatField(default=0.0)    # between 0 and 1 , with 1 being super reliable

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Data Source"


class Organisation(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    name = models.CharField(max_length=1000)
    fullname = models.CharField(max_length=1000, null=True, blank=True)
    org_path = models.CharField(max_length=5000, null=True, blank=True) # pocandora
    nesting = models.CharField(max_length=5000, null=True, blank=True) # pocandora
    protection_profile = models.CharField(max_length=30, null=True, blank=True)
    iscert = models.BooleanField("Is a CERT", null=False, default=False, blank=False)
    #team_rep = models.ForeignKey('Person', related_name='person_org', null=True, blank=True)

    address = models.CharField(max_length=1000, null=True, blank=True) 

    # XXX FIXME: country can be m-to-n!
    country = models.ForeignKey(Countrycode)
    phone = JSONField(form_class=JSONListToNewlineField)
    emergency_phone = JSONField(form_class=JSONListToNewlineField)
    fax = JSONField(form_class=JSONListToNewlineField)
    other_communication = models.CharField(max_length=1000, null=True, blank=True)
    email = JSONField(form_class=JSONListToNewlineField, validator=validate_email)
    website = models.URLField(max_length=1000, verbose_name="Website URL", null=True, blank=True)
    timezone = models.CharField(max_length=10, null=True, blank=True)   # XXX FIXME: later have a real time zone field
    business_hh_start = models.TimeField(verbose_name="Business hours start", null=True, blank=True)
    business_hh_end = models.TimeField(verbose_name="Business hours end", null=True, blank=True)
    date_established = models.DateField("Date established", null=True, blank=True)
    pgp_key = models.ForeignKey(PGPKey, null=True, blank=True)

    confirmed = models.BooleanField("Confirmed to exist", null=False, default=False, blank=False)
    active = models.BooleanField("Still active", null=False, default=False, blank=False)
    source = models.ForeignKey(Source, null=True, blank=True)

    ti_url = models.CharField(max_length=1000, verbose_name="TI URL", null=True, blank=True)  # link to the TI DB
    first_url = models.CharField(max_length=1000, verbose_name="FIRST.org URL", null=True, blank=True)  # link to the  DB

    # meta
    created = models.DateTimeField("Created", auto_now=False, auto_now_add=True, editable=True, blank=True, null=True )
    last_updated = models.DateTimeField("Last updated", auto_now=True, auto_now_add=False, editable=True, blank=True, null=True )

    def __unicode__(self):
        return self.name


class OrganisationTel(models.Model):
    """ Note: this will come later. Later we will have a 1-n relationship
    between Organisation and Tel"""
    phone = models.CharField(max_length=128)
    organisation = models.ForeignKey(Organisation)

    def __unicode__(self):
        return self.phone

class OrganisationEmail(models.Model):
    """ Note: this will come later. Later we will have a 1-n relationship
    between Organisation and Email"""
    email = models.EmailField(max_length=256)
    organisation = models.ForeignKey(Organisation)

    def __unicode__(self):
        return self.email


class Tag(models.Model):
    """ Note: each object can be assigned some 'tag'. Currently this is only implemented for organisations
    We use this to map organisations to for example 'national CERT', 'Energy sector CERT' etc
    """
    name    = models.CharField(max_length=128)

class Person(models.Model):
    # This field is required.
    user = models.OneToOneField(User, null=True)
    organisation = models.ForeignKey(Organisation)
    orgPocType  = models.CharField(max_length=30, null=True, blank=True)    # very pocandora specific!!
    title = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(upload_to="/static/person/pics/")
    phone = JSONField(form_class=JSONListToNewlineField)
    emergency_phone = JSONField(form_class=JSONListToNewlineField)
    fax = JSONField(form_class=JSONListToNewlineField)
    email = JSONField(form_class=JSONListToNewlineField)
    pgp_key = models.ForeignKey(PGPKey, null=True, blank=True)
    im = models.CharField(max_length=256, verbose_name="Instant Messenger ID", null=True, blank=True)   # instant messenger
    website = models.URLField(max_length=1000, verbose_name="Website URL", null=True, blank=True)
    timezone = models.CharField(max_length=10, null=True, blank=True)   # XXX FIXME: later have a real time zone field

    remarks = models.TextField()

    last_logged_in = models.TimeField(verbose_name="Last logged in")

    def __unicode__(self):
        return self.name

class NetObject(models.Model):

    source = models.ForeignKey(Source, null=True, blank=True)
    editor = models.ForeignKey(User, null=True)
    created = models.DateTimeField("Created", auto_now=False, auto_now_add=True, editable=True, blank=True, null=True)
    last_updated = models.DateTimeField("Last updated", auto_now=True, auto_now_add=False, editable=True, blank=True, null=True)

    class Meta:
        verbose_name = "NetObject"
        verbose_name_plural = "NetObjects"

class ASN(NetObject):
    asn = models.IntegerField(primary_key=True)
    asname = models.CharField(max_length=500)

    def __unicode__(self):
        return self.asn

class Inetnum(NetObject):
    inet = models.GenericIPAddressField()
    init_ip = models.GenericIPAddressField(editable=False, blank=True, null=True)
    end_ip = models.GenericIPAddressField(editable=False, blank=True, null=True)
    prefix_length = models.PositiveSmallIntegerField(editable=False, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.inet)

class IPAddress(NetObject):
    ip = models.GenericIPAddressField()

    def __unicode__(self):
        return self.ip


class Hostname(NetObject):
    fqdn = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.fqdn


class Domainname(NetObject):
    domain = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.domain


# FIXME: Why not part of the NetObject itself?
# FIXME: Assume an organisation hires another organisation to handle all
# abuse events from it's network... would this model cope with that 
# situation?
class NetObjContactLink(models.Model):
    netobj_link = models.ForeignKey(NetObject)
    # XXX FIXME: person or object should be subclasses of "Entity". Then have one link to Entity
    person_link = models.ForeignKey(Person)
    organisation_link = models.ForeignKey(Organisation)

    # how good is the contact link?
    quality = models.FloatField(default=0.0)    
    active = models.BooleanField(default=False) 
    weight = models.FloatField(default=0.1)
    created = models.DateTimeField("Created", auto_now=False, auto_now_add=True, editable=True, blank=True, null=True)
    last_updated = models.DateTimeField("Last updated", auto_now=True, auto_now_add=False, editable=True, blank=True, null=True)

