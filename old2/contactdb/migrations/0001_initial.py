# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Countrycode'
        db.create_table('contactdb_countrycode', (
            ('cc', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('cc3', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('contactdb', ['Countrycode'])

        # Adding model 'AirportCode'
        db.create_table('contactdb_airportcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Countrycode'], null=True, blank=True)),
        ))
        db.send_create_signal('contactdb', ['AirportCode'])

        # Adding model 'PGPKey'
        db.create_table('contactdb_pgpkey', (
            ('pgp_key_id', self.gf('django.db.models.fields.CharField')(max_length=1000, primary_key=True)),
            ('pgp_key', self.gf('django.db.models.fields.TextField')()),
            ('pgp_key_email', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('pgp_key_trust', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pgp_key_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('pgp_key_expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('contactdb', ['PGPKey'])

        # Adding model 'Source'
        db.create_table('contactdb_source', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, primary_key=True)),
            ('reliability', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('contactdb', ['Source'])

        # Adding model 'Organisation'
        db.create_table('contactdb_organisation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Organisation'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('org_path', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True, blank=True)),
            ('nesting', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True, blank=True)),
            ('protection_profile', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('housenr', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pobox', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Countrycode'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('emergency_phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=1000, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('business_hh_start', self.gf('django.db.models.fields.TimeField')()),
            ('business_hh_end', self.gf('django.db.models.fields.TimeField')()),
            ('date_established', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pgp_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.PGPKey'], null=True, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Source'])),
            ('vouching_proposed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Proposed by', to=orm['auth.User'])),
            ('ti_url', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('first_url', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('contactdb', ['Organisation'])

        # Adding M2M table for field vouching_vouched_by on 'Organisation'
        db.create_table('contactdb_organisation_vouching_vouched_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organisation', models.ForeignKey(orm['contactdb.organisation'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('contactdb_organisation_vouching_vouched_by', ['organisation_id', 'user_id'])

        # Adding model 'Person'
        db.create_table('contactdb_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('organisation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Organisation'])),
        ))
        db.send_create_signal('contactdb', ['Person'])

        # Adding model 'NetObject'
        db.create_table('contactdb_netobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('quality', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=0.1)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contactdb.Source'], null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('contactdb', ['NetObject'])

        # Adding model 'ASN'
        db.create_table('contactdb_asn', (
            ('netobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contactdb.NetObject'], unique=True)),
            ('asn', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('asname', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('contactdb', ['ASN'])

        # Adding model 'Inetnum'
        db.create_table('contactdb_inetnum', (
            ('netobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contactdb.NetObject'], unique=True, primary_key=True)),
            ('inet', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
        ))
        db.send_create_signal('contactdb', ['Inetnum'])

        # Adding model 'IPAddress'
        db.create_table('contactdb_ipaddress', (
            ('netobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contactdb.NetObject'], unique=True, primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
        ))
        db.send_create_signal('contactdb', ['IPAddress'])

        # Adding model 'Hostname'
        db.create_table('contactdb_hostname', (
            ('netobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contactdb.NetObject'], unique=True, primary_key=True)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('contactdb', ['Hostname'])

        # Adding model 'Domainname'
        db.create_table('contactdb_domainname', (
            ('netobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contactdb.NetObject'], unique=True, primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('contactdb', ['Domainname'])


    def backwards(self, orm):
        
        # Deleting model 'Countrycode'
        db.delete_table('contactdb_countrycode')

        # Deleting model 'AirportCode'
        db.delete_table('contactdb_airportcode')

        # Deleting model 'PGPKey'
        db.delete_table('contactdb_pgpkey')

        # Deleting model 'Source'
        db.delete_table('contactdb_source')

        # Deleting model 'Organisation'
        db.delete_table('contactdb_organisation')

        # Removing M2M table for field vouching_vouched_by on 'Organisation'
        db.delete_table('contactdb_organisation_vouching_vouched_by')

        # Deleting model 'Person'
        db.delete_table('contactdb_person')

        # Deleting model 'NetObject'
        db.delete_table('contactdb_netobject')

        # Deleting model 'ASN'
        db.delete_table('contactdb_asn')

        # Deleting model 'Inetnum'
        db.delete_table('contactdb_inetnum')

        # Deleting model 'IPAddress'
        db.delete_table('contactdb_ipaddress')

        # Deleting model 'Hostname'
        db.delete_table('contactdb_hostname')

        # Deleting model 'Domainname'
        db.delete_table('contactdb_domainname')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 22, 16, 5, 1, 246893, tzinfo=<UTC>)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 22, 16, 5, 1, 246801, tzinfo=<UTC>)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contactdb.airportcode': {
            'Meta': {'object_name': 'AirportCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Countrycode']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contactdb.asn': {
            'Meta': {'object_name': 'ASN', '_ormbases': ['contactdb.NetObject']},
            'asn': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'asname': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'netobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contactdb.NetObject']", 'unique': 'True'})
        },
        'contactdb.countrycode': {
            'Meta': {'object_name': 'Countrycode'},
            'cc': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'cc3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'contactdb.domainname': {
            'Meta': {'object_name': 'Domainname', '_ormbases': ['contactdb.NetObject']},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'netobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contactdb.NetObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contactdb.hostname': {
            'Meta': {'object_name': 'Hostname', '_ormbases': ['contactdb.NetObject']},
            'fqdn': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'netobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contactdb.NetObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contactdb.inetnum': {
            'Meta': {'object_name': 'Inetnum', '_ormbases': ['contactdb.NetObject']},
            'inet': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'netobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contactdb.NetObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contactdb.ipaddress': {
            'Meta': {'object_name': 'IPAddress', '_ormbases': ['contactdb.NetObject']},
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'netobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contactdb.NetObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contactdb.netobject': {
            'Meta': {'object_name': 'NetObject'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Source']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.1'})
        },
        'contactdb.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'business_hh_end': ('django.db.models.fields.TimeField', [], {}),
            'business_hh_start': ('django.db.models.fields.TimeField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Countrycode']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_established': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'first_url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'housenr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'nesting': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'org_path': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Organisation']", 'null': 'True', 'blank': 'True'}),
            'pgp_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.PGPKey']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pobox': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'protection_profile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Source']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'ti_url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'vouching_proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Proposed by'", 'to': "orm['auth.User']"}),
            'vouching_vouched_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Vouched for by'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'contactdb.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contactdb.Organisation']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contactdb.pgpkey': {
            'Meta': {'object_name': 'PGPKey'},
            'pgp_key': ('django.db.models.fields.TextField', [], {}),
            'pgp_key_created': ('django.db.models.fields.DateTimeField', [], {}),
            'pgp_key_email': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'pgp_key_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pgp_key_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'primary_key': 'True'}),
            'pgp_key_trust': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'contactdb.source': {
            'Meta': {'object_name': 'Source'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'primary_key': 'True'}),
            'reliability': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['contactdb']
