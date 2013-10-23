from contactdb.models import Organisation, Person
from contactdb.models import PGPKey, PGPUid, Source, Countrycode
from contactdb.models import NetObject,ASN,Inetnum,IPAddress,Hostname,Domainname
from django.contrib import admin

from django.core.exceptions import ValidationError
from django import forms

class PGPUidAdminPage(admin.ModelAdmin):
    fields = ['pgp_key', 'pgp_email']

class OrganisationAdminPage(admin.ModelAdmin):
    #fields = ('name', 'iscert', 'country', 'email', 'phone', 'emergency_phone')
    list_display = ('name', 'iscert', 'country', 'email', 'phone', 'emergency_phone', 'business_hh_start', 'business_hh_end', 'timezone', 'pgp_key')
    #list_display = ('id', 'name', 'einzelpreis', 'ort','verwendungszweck', 'verantwortlicher', 'datum_letzte_inventur')
    search_fields = ['name' , 'email', 'country']
    list_filter = ['country']
    
class InetnumFormField(forms.GenericIPAddressField):
    def validate_ipv46_address(self, value):
        from django.core.validators import validate_ipv4_address, validate_ipv6_address
        try:
            validate_ipv4_address(value)
            return 'ipv4'
        except ValidationError:
            try:
                validate_ipv6_address(value)
                return 'ipv6'
            except ValidationError:
                raise ValidationError(_('Enter a valid IPv4 or IPv6 address.'), code='invalid')
                
    def validate_ipv46_cidr(self, value):
        if '/' in value:
            splitted = value.split('/')
            prot = self.validate_ipv46_address(splitted[0])
                
            if prot is 'ipv4':
                try:
                    ipv4_prefix = int(splitted[1])
                    if ipv4_prefix < 0 or ipv4_prefix > 32:
                        raise ValidationError(_('IPv4 prefix is not valid.'), code='invalid')
                except:
                    raise ValidationError(_('IPv4 prefix is not valid.'), code='invalid')
            elif prot is 'ipv6':
                try:
                    ipv6_prefix = int(splitted[1])
                    if ipv6_prefix < 0 or ipv6_prefix > 128:
                        raise ValidationError(_('IPv6 prefix is not valid.'), code='invalid')
                except:
                    raise ValidationError(_('IPv6 prefix is not valid.'), code='invalid')
        else:
            self.validate_ipv46_address(value)
        
    def run_validators(self, value):
        return self.validate_ipv46_cidr(value)
        
    def to_python(self, value):
        try:
            if '/' in value:
                splitted = value.split('/')
                toRet = super(InetnumFormField, self).to_python(splitted[0]) + '/' + splitted[1]
            else:
                toRet = super(InetnumFormField, self).to_python(splitted[0])
            
            return toRet
        except Exception, e:
            print 'To_Python returned an exception: %r' % e
    
class InetnumForm(forms.ModelForm):
    inet = InetnumFormField(required=True)
    save_inetnum = None
    
    class Meta:
        model = Inetnum
    
    def clean(self):
        toRet = super(InetnumForm, self).clean()
        self.data['inet'] = self.cleaned_data['inet']
        return toRet
            
    def full_clean(self):
        toRet = super(InetnumForm, self).full_clean()
        if 'inet' in self._errors:
            del self._errors['inet']
            
        self.cleaned_data['inet'] = self.data['inet']
        
        return toRet
    
class InetnumAdminPage(admin.ModelAdmin):
    form = InetnumForm
        
    def save_model(self, request, obj, form, change):
        #print 'Inetnum: ' + str(form.cleaned_data['inet'])
        obj.save()

admin.site.register(Organisation, OrganisationAdminPage)
admin.site.register(Person)

admin.site.register(PGPKey)
admin.site.register(Source)
admin.site.register(Countrycode)

admin.site.register(PGPUid, PGPUidAdminPage)
admin.site.register(Inetnum, InetnumAdminPage)
