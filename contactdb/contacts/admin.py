from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Address)
admin.site.register(AutonomousSystem)
admin.site.register(AutonomousSystemAutomatic)
#
#admin.site.register(ClassificationIdentifier)
#admin.site.register(ClassificationType)
admin.site.register(Contact)
#admin.site.register(ContactAutomatic)
admin.site.register(Format)
admin.site.register(Fqdn)
#admin.site.register(FqdnAutomatic)
#admin.site.register(Inhibition)
admin.site.register(Network)
#admin.site.register(NetworkAutomatic)
admin.site.register(OrgSector)
admin.site.register(Organisation)
#admin.site.register(OrganisationAutomatic)
#admin.site.register(OrganisationToAsn)
#admin.site.register(OrganisationToAsnAutomatic)
#admin.site.register(OrganisationToFqdn)
#admin.site.register(OrganisationToFqdnAutomatic)
#admin.site.register(OrganisationToNetwork)
#admin.site.register(OrganisationToNetworkAutomatic)
#admin.site.register(OrganisationToTemplate)
#admin.site.register(OrganisationToTemplateAutomatic)
admin.site.register(Role)
#admin.site.register(RoleAutomatic)
#admin.site.register(Sector)
admin.site.register(Template)
