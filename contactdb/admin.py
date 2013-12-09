from contactdb.models import Organisation, Person
from contactdb.models import PGPKey, PGPUid, Source, Countrycode
from contactdb.models import NetObject,ASN,Inetnum,IPAddress,Hostname,Domainname
from django.contrib import admin

from contactdb.inetnumadmin import InetnumAdminPage

from django.core.exceptions import ValidationError

class PGPUidAdminPage(admin.ModelAdmin):
    fields = ['pgp_key', 'pgp_email']

class OrganisationAdminPage(admin.ModelAdmin):
    #fields = ('name', 'iscert', 'country', 'email', 'phone', 'emergency_phone')
    list_display = ('name', 'iscert', 'country', 'email', 'phone', 'emergency_phone', 'business_hh_start', 'business_hh_end', 'timezone', 'pgp_key')
    #list_display = ('id', 'name', 'einzelpreis', 'ort','verwendungszweck', 'verantwortlicher', 'datum_letzte_inventur')
    search_fields = ['name' , 'email', 'country']
    list_filter = ['country']

admin.site.register(Organisation, OrganisationAdminPage)
admin.site.register(Person)

admin.site.register(PGPKey)
admin.site.register(Source)
admin.site.register(Countrycode)

admin.site.register(PGPUid, PGPUidAdminPage)
admin.site.register(Inetnum, InetnumAdminPage)
