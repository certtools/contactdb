from contactdb.models import Organisation, Person
from contactdb.models import PGPKey, PGPUid, Source, Countrycode
from contactdb.models import NetObject,ASN,Inetnum,Domainname
from contactdb.models import TelephoneNumber, Email, URL, CommunicationChannel, Tag
from django.contrib import admin

from contactdb.inetnumadmin import InetnumAdminPage

from django.core.exceptions import ValidationError

def createInlineAdmin(model_class, number_of_lines=0, key_name=None):
    class InlineAdmin(admin.TabularInline):
        model = model_class
        extra = number_of_lines
        fk_name = key_name
        
    return InlineAdmin

class PGPUidAdminPage(admin.ModelAdmin):
    fields = ['pgp_key', 'pgp_email']

class OrganisationAdminPage(admin.ModelAdmin):
    #fields = ('name', 'iscert', 'country', 'email', 'phone', 'emergency_phone')
    list_display = ('name', 'country', 'business_hh_start', 'business_hh_end', 'timezone', 'pgp_key')
    #list_display = ('id', 'name', 'einzelpreis', 'ort','verwendungszweck', 'verantwortlicher', 'datum_letzte_inventur')
    search_fields = ['name' , 'email', 'country']
    list_filter = ['country']
    inlines = [
                createInlineAdmin(TelephoneNumber, key_name='parent'),
                createInlineAdmin(Email, key_name='parent'),
                createInlineAdmin(URL, key_name='parent'),
                createInlineAdmin(CommunicationChannel, key_name='parent'),
#                createInlineAdmin(ProtectionProfile),
                createInlineAdmin(Tag),
              ]
              
class PersonAdminPage(admin.ModelAdmin):
    list_display = ('user', 'name', 'organisation', 'title', 'picture', 'pgp_key', 'timezone', 'remarks')
    exclude = ('last_logged_in', )
    # Maybe the pgp keys should be multiple, and the im should be a "CommunicationChannel"
    
    search_fields = ['name', 'user']
    inlines = [
                createInlineAdmin(TelephoneNumber, key_name='parent'),
                createInlineAdmin(Email, key_name='parent'),
                createInlineAdmin(URL, key_name='parent'),
                createInlineAdmin(CommunicationChannel, key_name='parent'),
#                createInlineAdmin(ProtectionProfile),
                createInlineAdmin(Tag),
              ]

admin.site.register(Organisation, OrganisationAdminPage)
admin.site.register(Person, PersonAdminPage)

admin.site.register(PGPKey)
admin.site.register(Source)
admin.site.register(Countrycode)

admin.site.register(PGPUid, PGPUidAdminPage)

admin.site.register(Inetnum, InetnumAdminPage)

