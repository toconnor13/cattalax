# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Visit.hour'
        db.add_column(u'dashboard_visit', 'hour',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=4, to=orm['dashboard.Hour']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Visit.hour'
        db.delete_column(u'dashboard_visit', 'hour_id')


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
            'over_month': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Month']"}),
            'over_week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Week']"}),
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
        u'dashboard.month': {
            'Meta': {'object_name': 'Month'},
            'avg_duration': ('django.db.models.fields.IntegerField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_no': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_bounces': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_entries': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_walkbys': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
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
            'first_visit': ('django.db.models.fields.BooleanField', [], {}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Hour']"}),
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
        },
        u'dashboard.week': {
            'Meta': {'object_name': 'Week'},
            'avg_duration': ('django.db.models.fields.IntegerField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_bounces': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_entries': ('django.db.models.fields.IntegerField', [], {}),
            'no_of_walkbys': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"}),
            'week_no': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dashboard']