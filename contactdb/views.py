from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contactdb.permissions import IsUserOrReadOnly
from contactdb.permissions import IsInOrgOrReadOnly
from contactdb.serializers import UserSerializer
from contactdb.serializers import GroupSerializer

from contactdb.models import Person
from contactdb.serializers import PersonSerializer

from contactdb.models import Organisation
from contactdb.serializers import OrganisationSerializer

from contactdb.models import Countrycode
from contactdb.serializers import CountrycodeSerializer

from contactdb.models import Source
from contactdb.serializers import SourceSerializer

from contactdb.models import Tag
from contactdb.serializers import TagSerializer

from contactdb.models import ASN
from contactdb.serializers import ASNSerializer

import gnupg
import os


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def PGPKey(request, fingerprint):
    if request.method == 'GET':
        gpg = gnupg.GPG(homedir=os.environ['GNUPGHOME'])
        key = gpg.export_keys(fingerprint)
        return Response({fingerprint: key})


class CountrycodeViewSet(viewsets.ModelViewSet):
    queryset = Countrycode.objects.all()
    serializer_class = CountrycodeSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,
                              TokenAuthentication)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsInOrgOrReadOnly,)

    def pre_save(self, obj):
        g, created = Group.objects.get_or_create(name=obj.name)
        if not self.request.user.is_staff:
            g.user_set.add(self.request.user)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly,)

    def pre_save(self, obj):
        if self.request.user.is_staff or obj.user == self.request.user:
            if obj.organisation is not None:
                g, created = Group.objects.get_or_create(
                    name=obj.organisation.name)
                if created or obj.organisation.name in \
                        self.request.user.groups.all():
                    # only allow to add an organisation to an user if the user
                    # doing so is in the organisation
                    g.user_set.add(self.request.user)
        else:
            raise PermissionDenied(detail='User of Person has to be you.')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ASNViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = ASN.objects.all()
    serializer_class = ASNSerializer
