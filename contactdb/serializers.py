from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from contactdb.models import Person
from contactdb.models import Organisation
from contactdb.models import Countrycode
from contactdb.models import Source


class CountrycodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Countrycode
        fields = ('cc', 'cc3', 'country_name', )


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Source
        fields = ('name', 'reliability')

class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('name', 'country', 'phone', 'emergency_phone', 'fax',
                  'email', 'source', )


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('user', 'organisation', 'phone',
                  'emergency_phone', 'fax', 'email',)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'groups', 'username')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')
