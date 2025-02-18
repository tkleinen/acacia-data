# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Network.bound'
        db.add_column(u'meetnet_network', 'bound',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Network.bound'
        db.delete_column(u'meetnet_network', 'bound')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.datasource': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'meetlocatie'),)", 'object_name': 'Datasource'},
            'autoupdate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'config': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'generator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Generator']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_download': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meetlocatie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasources'", 'to': u"orm['data.MeetLocatie']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Europe/Amsterdam'", 'max_length': '50', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': u"orm['auth.User']", 'to': u"orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'anonymous'", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'data.generator': {
            'Meta': {'ordering': "['name']", 'object_name': 'Generator'},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'data.meetlocatie': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('projectlocatie', 'name'),)", 'object_name': 'MeetLocatie'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '28992'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'projectlocatie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProjectLocatie']"}),
            'webcam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Webcam']", 'null': 'True', 'blank': 'True'})
        },
        u'data.parameter': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'datasource'),)", 'object_name': 'Parameter'},
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Datasource']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'line'", 'max_length': '20'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '10'})
        },
        u'data.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'dark-blue'", 'max_length': '50'})
        },
        u'data.projectlocatie': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('project', 'name'),)", 'object_name': 'ProjectLocatie'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.TabGroup']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '28992'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Project']"}),
            'webcam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Webcam']", 'null': 'True', 'blank': 'True'})
        },
        u'data.series': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parameter', 'name'),)", 'object_name': 'Series'},
            'aggregate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cumstart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cumsum': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'offset': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Parameter']", 'null': 'True', 'blank': 'True'}),
            'resample': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'scale': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'line'", 'max_length': '20', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': u"orm['auth.User']", 'to': u"orm['auth.User']"})
        },
        u'data.sourcefile': {
            'Meta': {'unique_together': "(('name', 'datasource'),)", 'object_name': 'SourceFile'},
            'cols': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'crc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sourcefiles'", 'to': u"orm['data.Datasource']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'rows': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': u"orm['auth.User']", 'to': u"orm['auth.User']"})
        },
        u'data.tabgroup': {
            'Meta': {'object_name': 'TabGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.ProjectLocatie']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'data.webcam': {
            'Meta': {'object_name': 'Webcam'},
            'admin': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video': ('django.db.models.fields.TextField', [], {})
        },
        u'meetnet.channel': {
            'Meta': {'object_name': 'Channel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'monfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetnet.MonFile']"}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'range': ('django.db.models.fields.FloatField', [], {}),
            'range_unit': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reference_level': ('django.db.models.fields.FloatField', [], {}),
            'reference_unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'meetnet.datalogger': {
            'Meta': {'ordering': "['serial']", 'object_name': 'Datalogger'},
            'baro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Series']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'depth': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "'ctd'", 'max_length': '50'}),
            'refpnt': ('django.db.models.fields.FloatField', [], {}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetnet.Screen']", 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'meetnet.loggerdatasource': {
            'Meta': {'ordering': "['name']", 'object_name': 'LoggerDatasource', '_ormbases': [u'data.Datasource']},
            u'datasource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['data.Datasource']", 'unique': 'True', 'primary_key': 'True'}),
            'logger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasources'", 'to': u"orm['meetnet.Datalogger']"})
        },
        u'meetnet.monfile': {
            'Meta': {'object_name': 'MonFile', '_ormbases': [u'data.SourceFile']},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'compstat': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'createdby': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'instrument_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'instrument_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'monfilename': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'num_channels': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'num_points': ('django.db.models.fields.IntegerField', [], {}),
            'sample_method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sample_period': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'sourcefile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['data.SourceFile']", 'unique': 'True', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'meetnet.network': {
            'Meta': {'object_name': 'Network'},
            'bound': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_round': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'next_round': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'meetnet.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'well': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetnet.Well']"})
        },
        u'meetnet.screen': {
            'Meta': {'ordering': "['well', 'nr']", 'unique_together': "(('well', 'nr'),)", 'object_name': 'Screen'},
            'bottom': ('django.db.models.fields.FloatField', [], {}),
            'chart': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'diameter': ('django.db.models.fields.FloatField', [], {'default': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.CharField', [], {'default': "'pvc'", 'max_length': '10'}),
            'nr': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'top': ('django.db.models.fields.FloatField', [], {}),
            'well': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetnet.Well']"})
        },
        u'meetnet.well': {
            'Meta': {'ordering': "['name']", 'object_name': 'Well'},
            'bro': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'chart': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'huisnummer': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '28992'}),
            'log': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'maaiveld': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetnet.Network']"}),
            'nitg': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'plaats': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'refpnt': ('django.db.models.fields.FloatField', [], {}),
            'straat': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        }
    }

    complete_apps = ['meetnet']