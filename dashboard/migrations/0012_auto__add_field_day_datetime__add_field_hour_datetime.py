# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Day.datetime'
        db.add_column(u'dashboard_day', 'datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 5, 0, 0)),
                      keep_default=False)

        # Adding field 'Hour.datetime'
        db.add_column(u'dashboard_hour', 'datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 5, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Day.datetime'
        db.delete_column(u'dashboard_day', 'datetime')

        # Deleting field 'Hour.datetime'
        db.delete_column(u'dashboard_hour', 'datetime')


    models = {
        u'dashboard.customer': {
            'Meta': {'object_name': 'Customer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac_addr': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'dashboard.day': {
            'Meta': {'object_name': 'Day'},
            'avg_duration': ('django.db.models.fields.IntegerField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_bounces': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_entries': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_walkbys': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dashboard.hour': {
            'Meta': {'object_name': 'Hour'},
            'avg_duration': ('django.db.models.fields.IntegerField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Day']"}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_bounces': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_entries': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_walkbys': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"})
        },
        u'dashboard.outlet': {
            'Meta': {'object_name': 'Outlet'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sensor_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dashboard.visit': {
            'Meta': {'object_name': 'Visit'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patron': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Customer']"}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"})
        },
        u'dashboard.walkby': {
            'Meta': {'object_name': 'Walkby'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"})
        }
    }

    complete_apps = ['dashboard']