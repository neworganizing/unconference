# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Participant.user'
        db.alter_column(u'thewall_participant', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth_email.User'], unique=True))
        # Adding unique constraint on 'Participant', fields ['user']
        db.create_unique(u'thewall_participant', ['user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Participant', fields ['user']
        db.delete_unique(u'thewall_participant', ['user_id'])


        # Changing field 'Participant.user'
        db.alter_column(u'thewall_participant', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth_email.User']))

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
        u'auth_email.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thewall.day': {
            'Meta': {'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 4, 21, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thewall.participant': {
            'Meta': {'object_name': 'Participant'},
            'attendeenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth_email.User']", 'unique': 'True'})
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
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Room']", 'null': 'True', 'blank': 'True'}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Slot']", 'null': 'True', 'blank': 'True'}),
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