# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SessionTag'
        db.create_table('session_sessiontag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('session', ['SessionTag'])

        # Adding model 'Day'
        db.create_table('session_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('day', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 11, 18, 0, 0))),
        ))
        db.send_create_signal('session', ['Day'])

        # Adding model 'Slot'
        db.create_table('session_slot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['session.Day'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('session', ['Slot'])

        # Adding model 'Venue'
        db.create_table('session_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('session', ['Venue'])

        # Adding model 'Room'
        db.create_table('session_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('floor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['session.Venue'])),
        ))
        db.send_create_signal('session', ['Room'])

        # Adding model 'Session'
        db.create_table('session_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['session.Slot'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['session.Room'])),
            ('difficulty', self.gf('django.db.models.fields.CharField')(default='Beginner', max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('session', ['Session'])

        # Adding M2M table for field presenters on 'Session'
        db.create_table('session_session_presenters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm['session.session'], null=False)),
            ('participant', models.ForeignKey(orm['participants.participant'], null=False))
        ))
        db.create_unique('session_session_presenters', ['session_id', 'participant_id'])

        # Adding M2M table for field tags on 'Session'
        db.create_table('session_session_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm['session.session'], null=False)),
            ('sessiontag', models.ForeignKey(orm['session.sessiontag'], null=False))
        ))
        db.create_unique('session_session_tags', ['session_id', 'sessiontag_id'])


    def backwards(self, orm):
        # Deleting model 'SessionTag'
        db.delete_table('session_sessiontag')

        # Deleting model 'Day'
        db.delete_table('session_day')

        # Deleting model 'Slot'
        db.delete_table('session_slot')

        # Deleting model 'Venue'
        db.delete_table('session_venue')

        # Deleting model 'Room'
        db.delete_table('session_room')

        # Deleting model 'Session'
        db.delete_table('session_session')

        # Removing M2M table for field presenters on 'Session'
        db.delete_table('session_session_presenters')

        # Removing M2M table for field tags on 'Session'
        db.delete_table('session_session_tags')


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
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 18, 0, 0)'}),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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