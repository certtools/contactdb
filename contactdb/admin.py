from contactdb.models import Organisation, Person
from contactdb.models import Source, Countrycode
from contactdb.models import NetObject,ASN,Inetnum,DomainName
from contactdb.models import OtherCommunicationChannel, OTRFingerprint
from django.contrib import admin

from contactdb.inetnumadmin import InetnumAdminPage

from django.core.exceptions import ValidationError

def createInlineAdmin(model_class, number_of_lines=0, key_name=None):
    class InlineAdmin(admin.TabularInline):
        model = model_class
        extra = number_of_lines
        fk_name = key_name
        
    return InlineAdmin


class OrganisationAdminPage(admin.ModelAdmin):
    filter_horizontal = ['countrycodes', 'tags']
    fields = ('name', 'long_name', 'countrycodes', ('email', 'pgp_fingerprint'), 'phone_number', 'url', 'business_hh_start', 'business_hh_end', 'comment', 'tags')
    search_fields = ['name' , 'email']
    inlines = [
                createInlineAdmin(OtherCommunicationChannel),
              ]


class PersonAdminPage(admin.ModelAdmin):
    filter_horizontal = ['countrycodes', 'tags']
    fields = ('name', 'long_name', 'user', 'countrycodes', ('email', 'pgp_fingerprint'), 'phone_number', 'jabber_handle', 'organisation', 'picture', 'comment', 'tags')
    search_fields = ['name', 'user']
    inlines = [
                createInlineAdmin(OTRFingerprint),
                createInlineAdmin(OtherCommunicationChannel),
              ]
              
    exclude = ('last_logged_in', )


admin.site.register(Organisation, OrganisationAdminPage)
admin.site.register(Person, PersonAdminPage)

admin.site.register(Source)
admin.site.register(Countrycode)

admin.site.register(Inetnum, InetnumAdminPage)
