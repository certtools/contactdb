from django.conf.urls import patterns, include, url
from tastypie.api import Api
from contactdb.api.resources import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from contactdb.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


## ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#    model = User
#
#class GroupViewSet(viewsets.ModelViewSet):
#    model = Group



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)



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

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## Contact Web UI:
    #url(r'^$', 'contactdb.views.index', name='index'),
    #url(r'^search', 'contactdb.views.search', name='search'),
    #url(r'^addasn', 'contactdb.views.addasn', name='addasn'),
    #url(r'^addsource', 'contactdb.views.addsource', name='addsource'),
    # url(r'^certdir/', include('certdir.foo.urls')),

    ## django-rest-framework
    ##url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    ## Tastypie
    #(r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
