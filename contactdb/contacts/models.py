# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    id = models.IntegerField(primary_key=True),
    is_postal_address = models.BooleanField(null=True, blank=True),
    postal_address = models.CharField(max_length=1000)
    zip = models.IntegerField()
    country = models.CharField(max_length=2)
    tel = models.CharField(max_length=200)
    comment = models.TextField()

    def __str__(self):
        return self.postal_address + ", " + str(self.zip) + " (" + self.country + ")"

    class Meta:
        managed = False
        db_table = 'address'


class AutonomousSystem(models.Model):
    number = models.BigIntegerField(primary_key=True)
    ripe_aut_num = models.CharField(max_length=100, blank=True, null=True, help_text='ASN in the RIPE DB')
    comment = models.TextField()

    def __str__(self):
        return str(self.number)

    class Meta:
        managed = False
        db_table = 'autonomous_system'


class AutonomousSystemAutomatic(models.Model):
    number = models.BigIntegerField(primary_key=True)
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    ripe_aut_num = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'autonomous_system_automatic'


class ClassificationIdentifier(models.Model):
    name = models.TextField(unique=True, primary_key=True)

    class Meta:
        managed = False
        db_table = 'classification_identifier'


class ClassificationType(models.Model):
    name = models.CharField(unique=True, max_length=100, primary_key=True)

    class Meta:
        managed = False
        db_table = 'classification_type'


class Contact(models.Model):
    active = models.BooleanField()
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    tel = models.CharField(max_length=500, blank=True , null=True)
    fax = models.CharField(max_length=500, blank=True , null=True)
    mobile = models.CharField(max_length=500, blank=True , null=True)
    tel_priv = models.CharField(max_length=500, blank=True , null=True)
    mobile_priv = models.CharField(max_length=500, blank=True , null=True)
    pgp_key_id = models.CharField(max_length=128, blank=True , null=True)
    email = models.CharField(max_length=100)
    email_priv = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True , null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    format = models.ForeignKey('Format', models.DO_NOTHING, blank=True , null=True)
    organisation = models.ForeignKey('Organisation', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    picture = models.BinaryField(blank=True,  null=True)
    smime_certificate = models.BinaryField(blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    vouched_by = models.ForeignKey('self', models.DO_NOTHING, db_column='vouched_by', related_name='vouched_by1', null=True, blank=True)
    maintained_by = models.ForeignKey('self', models.DO_NOTHING, db_column='maintained_by', blank=True, null=True, related_name='maintained_by1')

    def __str__(self):
        return self.lastname + "," + self.firstname

    class Meta:
        managed = False
        db_table = 'contact'
    


class ContactAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    active = models.BooleanField()
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    tel = models.CharField(max_length=500)
    fax = models.CharField(max_length=500)
    mobile = models.CharField(max_length=500)
    tel_priv = models.CharField(max_length=500)
    mobile_priv = models.CharField(max_length=500)
    pgp_key_id = models.CharField(max_length=128)
    email = models.CharField(max_length=100)
    email_priv = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=500)
    birthdate = models.DateTimeField(blank=True, null=True)
    format = models.ForeignKey('Format', models.DO_NOTHING)
    organisation_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField()
    picture = models.BinaryField(blank=True, null=True)
    smime_certificate = models.BinaryField(blank=True, null=True)
    address_id = models.IntegerField(blank=True, null=True)
    vouched_by = models.IntegerField()
    maintained_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_automatic'


class Format(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'format'


class Fqdn(models.Model):
    fqdn = models.TextField(unique=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'fqdn'


class FqdnAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    fqdn = models.TextField(unique=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'fqdn_automatic'


class Inhibition(models.Model):
    asn = models.ForeignKey(AutonomousSystem, models.DO_NOTHING, blank=True, null=True)
    net = models.ForeignKey('Network', models.DO_NOTHING, blank=True, null=True)
    classification_type = models.ForeignKey(ClassificationType, models.DO_NOTHING, blank=True, null=True)
    classification_identifier = models.ForeignKey(ClassificationIdentifier, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'inhibition'


class Network(models.Model):
    address = models.TextField(unique=True)  # This field type is a guess.
    comment = models.TextField()

    def __str__(self):
        return str(self.address)

    class Meta:
        managed = False
        db_table = 'network'


class NetworkAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    address = models.TextField(unique=True)  # This field type is a guess.
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'network_automatic'


class OrgSector(models.Model):
    organisation = models.ForeignKey('Organisation', models.DO_NOTHING, blank=True, null=True)
    sector = models.ForeignKey('Sector', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'org_sector'


class Organisation(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500)
    sector = models.ForeignKey('Sector', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField()
    ripe_org_hdl = models.CharField(max_length=100, blank=True, null=True)
    ti_handle = models.CharField(max_length=500, blank=True, null=True)
    first_handle = models.CharField(max_length=500, blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name 

    class Meta:
        managed = False
        db_table = 'organisation'


class OrganisationAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    parent_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500)
    sector = models.ForeignKey('Sector', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField()
    ripe_org_hdl = models.CharField(max_length=100, blank=True, null=True)
    ti_handle = models.CharField(max_length=500, blank=True, null=True)
    first_handle = models.CharField(max_length=500, blank=True, null=True)
    address_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organisation_automatic'


class OrganisationToAsn(models.Model):
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    asn = models.ForeignKey(AutonomousSystem, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_asn'
        unique_together = (('organisation', 'asn'),)


class OrganisationToAsnAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    organisation = models.ForeignKey(OrganisationAutomatic, models.DO_NOTHING)
    asn = models.ForeignKey(AutonomousSystemAutomatic, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_asn_automatic'
        unique_together = (('organisation', 'asn'),)


class OrganisationToFqdn(models.Model):
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    fqdn = models.ForeignKey(Fqdn, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_fqdn'
        unique_together = (('organisation', 'fqdn'),)


class OrganisationToFqdnAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    organisation = models.ForeignKey(OrganisationAutomatic, models.DO_NOTHING)
    fqdn = models.ForeignKey(FqdnAutomatic, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_fqdn_automatic'
        unique_together = (('organisation', 'fqdn'),)


class OrganisationToNetwork(models.Model):
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    net = models.ForeignKey(Network, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_network'
        unique_together = (('organisation', 'net'),)


class OrganisationToNetworkAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    organisation = models.ForeignKey(OrganisationAutomatic, models.DO_NOTHING)
    net = models.ForeignKey(NetworkAutomatic, models.DO_NOTHING)
    notification_interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organisation_to_network_automatic'
        unique_together = (('organisation', 'net'),)


class OrganisationToTemplate(models.Model):
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    template = models.ForeignKey('Template', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_to_template'


class OrganisationToTemplateAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    organisation = models.ForeignKey(OrganisationAutomatic, models.DO_NOTHING)
    template = models.ForeignKey('Template', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organisation_to_template_automatic'


class Role(models.Model):
    role_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_primary_contact = models.BooleanField()
    is_secondary_contact = models.BooleanField()
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    contact = models.ForeignKey(Contact, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role'


class RoleAutomatic(models.Model):
    import_source = models.CharField(max_length=500)
    import_time = models.DateTimeField()
    role_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_primary_contact = models.BooleanField()
    is_secondary_contact = models.BooleanField()
    organisation = models.ForeignKey(OrganisationAutomatic, models.DO_NOTHING)
    contact = models.ForeignKey(ContactAutomatic, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role_automatic'


class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'sector'


class Template(models.Model):
    path = models.CharField(max_length=200)
    classification_type = models.ForeignKey(ClassificationType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'template'
