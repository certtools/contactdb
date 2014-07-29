import django_filters

from contactdb.models import Organisation


class OrganisationFilter(django_filters.FilterSet):

    class Meta:
        model = Organisation
        fields = ['name']
