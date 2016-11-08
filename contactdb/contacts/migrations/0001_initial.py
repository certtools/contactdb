# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-07 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_address', models.CharField(max_length=1000)),
                ('zip', models.IntegerField()),
                ('country', models.CharField(max_length=2)),
                ('tel', models.CharField(max_length=200)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'address',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AutonomousSystem',
            fields=[
                ('number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ripe_aut_num', models.CharField(blank=True, help_text='ASN in the RIPE DB', max_length=100, null=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'autonomous_system',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AutonomousSystemAutomatic',
            fields=[
                ('number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('ripe_aut_num', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'autonomous_system_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClassificationIdentifier',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'classification_identifier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClassificationType',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'classification_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('firstname', models.CharField(max_length=500)),
                ('lastname', models.CharField(max_length=500)),
                ('tel', models.CharField(max_length=500)),
                ('fax', models.CharField(max_length=500)),
                ('mobile', models.CharField(max_length=500)),
                ('tel_priv', models.CharField(max_length=500)),
                ('mobile_priv', models.CharField(max_length=500)),
                ('pgp_key_id', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=100)),
                ('email_priv', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(max_length=500)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('picture', models.BinaryField(blank=True, null=True)),
                ('smime_certificate', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('firstname', models.CharField(max_length=500)),
                ('lastname', models.CharField(max_length=500)),
                ('tel', models.CharField(max_length=500)),
                ('fax', models.CharField(max_length=500)),
                ('mobile', models.CharField(max_length=500)),
                ('tel_priv', models.CharField(max_length=500)),
                ('mobile_priv', models.CharField(max_length=500)),
                ('pgp_key_id', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=100)),
                ('email_priv', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(max_length=500)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('organisation_id', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('picture', models.BinaryField(blank=True, null=True)),
                ('smime_certificate', models.BinaryField(blank=True, null=True)),
                ('address_id', models.IntegerField(blank=True, null=True)),
                ('vouched_by', models.IntegerField()),
                ('maintained_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'contact_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'format',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fqdn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fqdn', models.TextField(unique=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'fqdn',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FqdnAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('fqdn', models.TextField(unique=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'fqdn_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Inhibition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'inhibition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(unique=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'network',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NetworkAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('address', models.TextField(unique=True)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'network_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=500)),
                ('comment', models.TextField()),
                ('ripe_org_hdl', models.CharField(blank=True, max_length=100, null=True)),
                ('ti_handle', models.CharField(blank=True, max_length=500, null=True)),
                ('first_handle', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'organisation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=500)),
                ('comment', models.TextField()),
                ('ripe_org_hdl', models.CharField(blank=True, max_length=100, null=True)),
                ('ti_handle', models.CharField(blank=True, max_length=500, null=True)),
                ('first_handle', models.CharField(blank=True, max_length=500, null=True)),
                ('address_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'organisation_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToAsn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_asn',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToAsnAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_asn_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToFqdn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_fqdn',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToFqdnAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_fqdn_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_network',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToNetworkAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('notification_interval', models.IntegerField()),
            ],
            options={
                'db_table': 'organisation_to_network_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'organisation_to_template',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationToTemplateAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'organisation_to_template_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrgSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'org_sector',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.TextField(blank=True, null=True)),
                ('is_primary_contact', models.BooleanField()),
                ('is_secondary_contact', models.BooleanField()),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoleAutomatic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_source', models.CharField(max_length=500)),
                ('import_time', models.DateTimeField()),
                ('role_type', models.TextField(blank=True, null=True)),
                ('is_primary_contact', models.BooleanField()),
                ('is_secondary_contact', models.BooleanField()),
            ],
            options={
                'db_table': 'role_automatic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'sector',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'template',
                'managed': False,
            },
        ),
    ]
