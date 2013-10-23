from django.conf.urls import patterns, include, url
from tastypie.api import Api
from contactdb.api.resources import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Add support for tastypie
v1_api = Api(api_name='v1')
v1_api.register(Country())
v1_api.register(PGPKey())
v1_api.register(PGPUid())
v1_api.register(Source())
v1_api.register(Organisation())
v1_api.register(OrganisationTel())
v1_api.register(OrganisationEmail())
v1_api.register(Person())
v1_api.register(NetObject())
v1_api.register(ASN())
v1_api.register(Inetnum())
v1_api.register(IPAddress())
v1_api.register(Hostname())
v1_api.register(Domainname())
v1_api.register(NetObjContactLink())


urlpatterns = patterns('',
    # Contact Web UI:
    url(r'^$', 'contactdb.views.index', name='index'),
    url(r'^search', 'contactdb.views.search', name='search'),
    url(r'^addasn', 'contactdb.views.addasn', name='addasn'),
    url(r'^addsource', 'contactdb.views.addsource', name='addsource'),
    # url(r'^certdir/', include('certdir.foo.urls')),

    # Tastypie
    (r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
