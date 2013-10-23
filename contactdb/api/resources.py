from tastypie.resources import ModelResource
from tastypie.constants import ALL
from contactdb.models import *


# NOTE: these classes are semi-automatically generated via scripts/gen-api.sh


class Country(ModelResource):
    class Meta:
        filtering = {
                        "country_name" : ("exact", "startswith", "contains") 
                    }

        queryset = Countrycode.objects.all()
        allowed_methods = ['get']


class PGPKey(ModelResource):
    class Meta:
        queryset = PGPKey.objects.all()
        allowed_methods = ['get']


class PGPUid(ModelResource):
    class Meta:
        queryset = PGPUid.objects.all()
        allowed_methods = ['get']


class Source(ModelResource):
    class Meta:
        queryset = Source.objects.all()
        allowed_methods = ['get']


class Organisation(ModelResource):
    class Meta:
        queryset = Organisation.objects.all()
        allowed_methods = ['get']


class OrganisationTel(ModelResource):
    class Meta:
        queryset = OrganisationTel.objects.all()
        allowed_methods = ['get']


class OrganisationEmail(ModelResource):
    class Meta:
        queryset = OrganisationEmail.objects.all()
        allowed_methods = ['get']


class Person(ModelResource):
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get']



class NetObject(ModelResource):
    class Meta:
        queryset = NetObject.objects.all()
        allowed_methods = ['get']

class NetObjContactLink(ModelResource):
    class Meta:
        #queryset = NetObjContactLink.objects.all()
        allowed_methods = []

class ASN(ModelResource):
    class Meta:
        queryset = ASN.objects.all()
        allowed_methods = ['get']


class Inetnum(ModelResource):
    class Meta:
        queryset = Inetnum.objects.all()
        allowed_methods = ['get']


class IPAddress(ModelResource):
    class Meta:
        queryset = IPAddress.objects.all()
        allowed_methods = ['get']


class Hostname(ModelResource):
    class Meta:
        queryset = Hostname.objects.all()
        allowed_methods = ['get']


class Domainname(ModelResource):
    class Meta:
        queryset = Domainname.objects.all()
        allowed_methods = ['get']



