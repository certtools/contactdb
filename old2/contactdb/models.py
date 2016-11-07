from django.db.models import Model, CharField, FloatField, ForeignKey, \
    EmailField, TextField, DateTimeField, TimeField, BooleanField, \
    DateField, ImageField, URLField, IntegerField, ManyToManyField, \
    OneToOneField
from django.contrib.auth.models import User

from contactdb.inetnum import InetnumModel

from datetime import datetime

MEDIA_ROOT = '/var/www/upload/'
MEDIA_URL = '/upload/'

# Auto generate an auth token for all the users

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# ---------------------------------------------


class Countrycode(Model):
    # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    # we can load this automatically from ripe.NET
    cc = CharField(max_length=2, primary_key=True)
    country_name = CharField(max_length=100)

    def __unicode__(self):
        return self.country_name

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"


class Source(Model):
    name = CharField(max_length=50, primary_key=True)
    reliability = FloatField(default=0.0)  # between 0 and 1, with 1 being super reliable

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "data source"


class Tag(Model):
    name = CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.name


class Entity(Model):
    name = CharField(max_length=50)
    long_name = CharField(max_length=1000, null=True, blank=True)

    ####################
    countrycodes = ManyToManyField(Countrycode, related_name="%(app_label)s_%(class)s", blank=True, null=True)
    tags = ManyToManyField(Tag, related_name="%(app_label)s_%(class)s", blank=True, null=True)
    ####################

    source = ForeignKey(Source, null=True, blank=True)

    email = EmailField(null=False)
    pgp_fingerprint = CharField(max_length=50, null=True, blank=True)

    phone_number = CharField(max_length=30, null=True, blank=True)
    url = URLField("URL", null=True, blank=True)
    comment = TextField(max_length=1000, null=True, blank=True)

    created = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Organisation(Entity):
    address = TextField(max_length=1000, null=True, blank=True)

    business_hh_start = TimeField(verbose_name="business hours start",
                                  null=True, blank=True)
    business_hh_end = TimeField(verbose_name="business hours end",
                                null=True, blank=True)
    date_established = DateField(verbose_name="date established",
                                 null=True, blank=True)

    confirmed = BooleanField(verbose_name="confirmed to exist", default=False)
    active = BooleanField(verbose_name="still active", default=False)

    ti_url = CharField(max_length=500, null=True, blank=True)
    first_url = CharField(max_length=500, null=True, blank=True)


class Person(Entity):
    user = OneToOneField(User, related_name='persons', null=True, blank=True)
    organisations = ManyToManyField(Organisation, related_name="%(app_label)s_%(class)s", blank=True, null=True)
    picture = ImageField(upload_to='/static/person/pics/', null=True, blank=True)
    last_logged_in = TimeField(null=False, default=datetime.now)

    jabber_handle = EmailField(max_length=100, null=True, blank=True)


class CommunicationChannel(Model):
    description = CharField(max_length=200, null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OTRFingerprint(Model):
    otr_fingerprint = CharField(max_length=50, null=False)
    handle = ForeignKey(Person, related_name='otr_fingerprints')


class OtherCommunicationChannel(CommunicationChannel):
    entity = ForeignKey(Entity)
    value = CharField("communication channel", max_length=1000, null=False,
                      blank=False)
    channel_type = CharField(max_length=100, null=False)

    class Meta:
        verbose_name = "communication channel"


class NetObject(Model):
    active = BooleanField(default=False)

    source = ForeignKey(Source, null=True)
    owners = ManyToManyField(Entity, related_name="%(app_label)s_%(class)s")
    created = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ASN(NetObject):
    asn = IntegerField(primary_key=True)
    asname = CharField(max_length=500)

    def __unicode__(self):
        return str(self.asn)

    class Meta:
        verbose_name = "Autonomous System Number"
        verbose_name_plural = "Autonomous System Numbers"


class Inetnum(NetObject, InetnumModel):
    pass


class DomainName(NetObject):
    domain = CharField(max_length=1000)

    def __unicode__(self):
        return self.domain


class TLD(NetObject):
    tld = CharField(max_length=100, primary_key=True)

    def __unicode__(self):
        return self.tld
