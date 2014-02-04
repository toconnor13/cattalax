# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'dashboard_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mac_addr', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'dashboard', ['Customer'])

        # Adding model 'Outlet'
        db.create_table(u'dashboard_outlet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('sensor_no', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['Outlet'])

        # Adding model 'Visit'
        db.create_table(u'dashboard_visit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patron', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Customer'])),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Outlet'])),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('arrival_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['Visit'])

        # Adding model 'Walkby'
        db.create_table(u'dashboard_walkby', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Outlet'])),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['Walkby'])

        # Adding model 'Day'
        db.create_table(u'dashboard_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Outlet'])),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_walkbys', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_entries', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_bounces', self.gf('django.db.models.fields.IntegerField')()),
            ('avg_duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['Day'])

        # Adding model 'Hour'
        db.create_table(u'dashboard_hour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Day'])),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Outlet'])),
            ('no_of_walkbys', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_entries', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_bounces', self.gf('django.db.models.fields.IntegerField')()),
            ('avg_duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['Hour'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'dashboard_customer')

        # Deleting model 'Outlet'
        db.delete_table(u'dashboard_outlet')

        # Deleting model 'Visit'
        db.delete_table(u'dashboard_visit')

        # Deleting model 'Walkby'
        db.delete_table(u'dashboard_walkby')

        # Deleting model 'Day'
        db.delete_table(u'dashboard_day')

        # Deleting model 'Hour'
        db.delete_table(u'dashboard_hour')


    models = {
        u'dashboard.customer': {
            'Meta': {'object_name': 'Customer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac_addr': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'dashboard.day': {
            'Meta': {'object_name': 'Day'},
            'avg_duration': ('django.db.models.fields.IntegerField', [], {}),
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
            'arrival_time': ('django.db.models.fields.IntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patron': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Customer']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"})
        },
        u'dashboard.walkby': {
            'Meta': {'object_name': 'Walkby'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Outlet']"})
        }
    }

    complete_apps = ['dashboard']