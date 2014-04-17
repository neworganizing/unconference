# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table(u'thewall_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('attendeenumber', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'thewall', ['Participant'])

        # Adding model 'SessionTag'
        db.create_table(u'thewall_sessiontag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'thewall', ['SessionTag'])

        # Adding model 'Day'
        db.create_table(u'thewall_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('day', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 4, 17, 0, 0))),
        ))
        db.send_create_signal(u'thewall', ['Day'])

        # Adding model 'Slot'
        db.create_table(u'thewall_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Day'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'thewall', ['Slot'])

        # Adding model 'Venue'
        db.create_table(u'thewall_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'thewall', ['Venue'])

        # Adding model 'Room'
        db.create_table(u'thewall_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('floor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Venue'])),
        ))
        db.send_create_signal(u'thewall', ['Room'])

        # Adding model 'Session'
        db.create_table(u'thewall_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('headline', self.gf('django.db.models.fields.TextField')()),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Slot'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Room'])),
            ('difficulty', self.gf('django.db.models.fields.CharField')(default='Beginner', max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'thewall', ['Session'])

        # Adding M2M table for field presenters on 'Session'
        m2m_table_name = db.shorten_name(u'thewall_session_presenters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'thewall.session'], null=False)),
            ('participant', models.ForeignKey(orm[u'thewall.participant'], null=False))
        ))
        db.create_unique(m2m_table_name, ['session_id', 'participant_id'])

        # Adding M2M table for field tags on 'Session'
        m2m_table_name = db.shorten_name(u'thewall_session_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'thewall.session'], null=False)),
            ('sessiontag', models.ForeignKey(orm[u'thewall.sessiontag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['session_id', 'sessiontag_id'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table(u'thewall_participant')

        # Deleting model 'SessionTag'
        db.delete_table(u'thewall_sessiontag')

        # Deleting model 'Day'
        db.delete_table(u'thewall_day')

        # Deleting model 'Slot'
        db.delete_table(u'thewall_slot')

        # Deleting model 'Venue'
        db.delete_table(u'thewall_venue')

        # Deleting model 'Room'
        db.delete_table(u'thewall_room')

        # Deleting model 'Session'
        db.delete_table(u'thewall_session')

        # Removing M2M table for field presenters on 'Session'
        db.delete_table(db.shorten_name(u'thewall_session_presenters'))

        # Removing M2M table for field tags on 'Session'
        db.delete_table(db.shorten_name(u'thewall_session_tags'))


    models = {
        u'thewall.day': {
            'Meta': {'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 4, 17, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thewall.participant': {
            'Meta': {'object_name': 'Participant'},
            'attendeenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thewall.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Venue']"})
        },
        u'thewall.session': {
            'Meta': {'object_name': 'Session'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'difficulty': ('django.db.models.fields.CharField', [], {'default': "'Beginner'", 'max_length': '30'}),
            'headline': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'presenters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['thewall.Participant']", 'symmetrical': 'False'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Room']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Slot']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['thewall.SessionTag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'thewall.sessiontag': {
            'Meta': {'object_name': 'SessionTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'thewall.slot': {
            'Meta': {'ordering': "('day__day', 'start_time')", 'object_name': 'Slot'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Day']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'thewall.venue': {
            'Meta': {'object_name': 'Venue'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['thewall']