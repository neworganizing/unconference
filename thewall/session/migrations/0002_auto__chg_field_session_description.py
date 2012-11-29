# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Session.description'
        db.alter_column('session_session', 'description', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Session.description'
        db.alter_column('session_session', 'description', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'participants.participant': {
            'Meta': {'object_name': 'Participant'},
            'attendeenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'session.day': {
            'Meta': {'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'session.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Venue']"})
        },
        'session.session': {
            'Meta': {'object_name': 'Session'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'difficulty': ('django.db.models.fields.CharField', [], {'default': "'Beginner'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'presenters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['participants.Participant']", 'symmetrical': 'False'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Room']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Slot']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['session.SessionTag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'session.sessiontag': {
            'Meta': {'object_name': 'SessionTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'session.slot': {
            'Meta': {'object_name': 'Slot'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Day']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'session.venue': {
            'Meta': {'object_name': 'Venue'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['session']