import django_filters

from contactdb.models import Organisation
from contactdb.models import Person


class OrganisationFilter(django_filters.FilterSet):

    class Meta:
        model = Organisation
        fields = ['name']


class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = Person
        fields = ['name']
