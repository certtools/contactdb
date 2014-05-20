from django.db import models
from django.contrib.auth.models import User
import django.core.validators
validate_url = django.core.validators.URLValidator()
validate_email = django.core.validators.validate_email

from contactdb.fields import JSONField
from contactdb.forms.fields import JSONListToNewlineField

MEDIA_ROOT = '/var/www/upload/'
MEDIA_URL = '/upload/'

# Auto generate an auth token for all the users

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# ---------------------------------------------

class ContactDBObject(models.Model):
    oid = models.AutoField(primary_key=True)
    created = models.DateTimeField("Created", auto_now=False, auto_now_add=True, editable=True, blank=True, null=True)
    last_updated = models.DateTimeField("Last updated", auto_now=True, auto_now_add=False, editable=True, blank=True, null=True)
    
class Tag(models.Model):
    ''' 
        Note: each object can be assigned some 'tag'. Currently this is only implemented for organi<ations
        We use this to map organizations to for example 'national CERT', 'Energy sector CERT' etc
    '''
    
    obj = models.ForeignKey(ContactDBObject)
    name = models.CharField(max_length=128)

class Countrycode(ContactDBObject):
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


class PGPKey(ContactDBObject):
    pgp_key_id = models.CharField(max_length=1000, primary_key=True)
    pgp_key = models.TextField(blank=True, null=True)
    pgp_key_created = models.DateTimeField("Created", null=True, blank=True)
    pgp_key_expires = models.DateTimeField("Expires", null=True, blank=True)
    
    def __unicode__(self):
        # return self.pgp_key_id + '(' + self.pgp_key_email + ')'
        return self.pgp_key_id
    
    class Meta:
        verbose_name = "PGP Key"


class PGPUid(ContactDBObject):
    pgp_email = models.EmailField(verbose_name="Email (UID)")
    pgp_key = models.ForeignKey(PGPKey)
    
    def __unicode__(self):
        return self.pgp_key.pgp_key_id + " <" + self.pgp_email + ">"
    
    class Meta:
        verbose_name = "PGP UID"
        verbose_name_plural = "PGP UIDs"


class Source(ContactDBObject):
    name = models.CharField(max_length=1000, primary_key=True)
    reliability = models.FloatField(default=0.0) # between 0 and 1, with 1 being super reliable

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Data Source"
        
class TelephoneNumber(ContactDBObject):
    parent = models.ForeignKey(ContactDBObject, related_name='phone_parent_object')
    number = models.CharField("Phone Number", max_length=30, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    
class Email(ContactDBObject):
    parent = models.ForeignKey(ContactDBObject, related_name='email_parent_object')
    value = models.EmailField("Email", null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    
class URL(ContactDBObject):
    parent = models.ForeignKey(ContactDBObject, related_name='url_parent_object')
    value = models.URLField("URL", null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    
class CommunicationChannel(ContactDBObject):
    parent = models.ForeignKey(ContactDBObject, related_name='channel_parent_object')
    value = models.CharField("Channel", max_length=1000, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)    
        
class Entity(ContactDBObject):
    entity_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=1000)
    
    country = models.ForeignKey(Countrycode) # XXX FIXME: country can be m-to-n
    pgp_key = models.ForeignKey(PGPKey, verbose_name="PGP Key", null=True, blank=True)
    
    timezone = models.CharField(max_length=10, null=True, blank=True) # XXX FIXME: later have a real time zone field
    source = models.ForeignKey(Source, null=True, blank=True)

class Organisation(Entity):
    shortname = models.CharField(max_length=1000, null=True, blank=True)
    
    # Phone Numbers, Email, Websites and other communication methods are available in the admin site but stored separately
    
    business_hh_start = models.TimeField(verbose_name="Business hours start", null=True, blank=True)
    business_hh_end = models.TimeField(verbose_name="Business hours end", null=True, blank=True)
    date_established = models.DateField(verbose_name="Date established", null=True, blank=True)
    
    confirmed = models.BooleanField(verbose_name="Confirmed to exist", null=False, default=False, blank=False)
    active = models.BooleanField(verbose_name="Still active", null=False, default=False, blank=False)
    
    ti_url = models.CharField(max_length=1000, verbose_name="TI URL", null=True, blank=True)
    first_url = models.CharField(max_length=1000, verbose_name="FIRST.org URL", null=True, blank=True)  # link to the  DB

    def __unicode__(self):
        return self.name

class Person(Entity):
    user = models.ForeignKey(User, related_name='persons')
    organisation = models.ForeignKey(Organisation)
    title = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to="/static/person/pics/")

    remarks = models.TextField()

    last_logged_in = models.TimeField(auto_now_add=True, verbose_name="Last logged in")

    def __unicode__(self):
        return self.name


class NetObject(ContactDBObject):
    quality = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)
    weight = models.FloatField(default=0.1)

    source = models.ForeignKey(Source, null=True, blank=True)
    editor = models.ForeignKey(User, null=True)
    owner = models.ForeignKey(Entity)

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


class Domainname(NetObject):
    domain = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.domain
