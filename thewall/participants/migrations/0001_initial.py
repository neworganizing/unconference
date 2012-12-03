# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table('participants_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('attendeenumber', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('participants', ['Participant'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table('participants_participant')


    models = {
        'participants.participant': {
            'Meta': {'object_name': 'Participant'},
            'attendeenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['participants']