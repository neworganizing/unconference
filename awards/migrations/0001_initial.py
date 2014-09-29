# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth import get_user_model

from awards.utils import get_user_profile_model, get_organization_model

# Support for custom profile
UserProfile = get_user_profile_model()
user_profile_app_label = UserProfile._meta.app_label
user_profile_orm_label = '%s.%s' % (
    UserProfile._meta.app_label,
    UserProfile._meta.object_name)

user_profile_model_label = '%s.%s' % (
    UserProfile._meta.app_label,
    UserProfile._meta.module_name)

# Support for custom organization
Organization = get_organization_model()
organization_app_label = Organization._meta.app_label
organization_orm_label = '%s.%s' % (
    Organization._meta.app_label,
    Organization._meta.object_name)

organization_model_label = '%s.%s' % (
    Organization._meta.app_label,
    Organization._meta.module_name)

# Support for custom user
User = get_user_model()
user_app_label = User._meta.app_label
user_orm_label = '%s.%s' % (
    User._meta.app_label,
    User._meta.object_name)

user_model_label = '%s.%s' % (
    User._meta.app_label,
    User._meta.module_name)


class Migration(SchemaMigration):

    depends_on = (
        (user_profile_app_label, "0001_initial"),
        (user_app_label, "0001_initial"),
        (organization_app_label, "0001_initial")
    )

    def forwards(self, orm):
        # Adding model 'MostValuableOrganizer'
        db.create_table(u'awards_mostvaluableorganizer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unconference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Unconference'])),
            ('nominator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluableorganizer_nominees', to=orm[user_profile_orm_label])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluableorganizer_nominations', to=orm[user_profile_orm_label])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contacted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('personal_statement', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=('unconference',), max_length=50, populate_from='profile')),
            ('innovation', self.gf('django.db.models.fields.TextField')()),
            ('respect', self.gf('django.db.models.fields.TextField')()),
            ('courage', self.gf('django.db.models.fields.TextField')()),
            ('excellence', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'awards', ['MostValuableOrganizer'])

        # Adding model 'MostValuableTechnology'
        db.create_table(u'awards_mostvaluabletechnology', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unconference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Unconference'])),
            ('nominator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluabletechnology_nominees', to=orm[user_profile_orm_label])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluabletechnology_nominations', to=orm[user_profile_orm_label])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contacted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('personal_statement', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=('unconference',), max_length=50, populate_from='name')),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mvt_nominations', to=orm[organization_orm_label])),
            ('innovation', self.gf('django.db.models.fields.TextField')()),
            ('potential', self.gf('django.db.models.fields.TextField')()),
            ('accessibility', self.gf('django.db.models.fields.TextField')()),
            ('additional', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'awards', ['MostValuableTechnology'])

        # Adding model 'MostValuableCampaign'
        db.create_table(u'awards_mostvaluablecampaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unconference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thewall.Unconference'])),
            ('nominator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluablecampaign_nominees', to=orm[user_profile_orm_label])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mostvaluablecampaign_nominations', to=orm[user_profile_orm_label])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contacted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('personal_statement', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=('unconference',), max_length=50, populate_from='name')),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mvc_nominations', to=orm[organization_orm_label])),
            ('innovation', self.gf('django.db.models.fields.TextField')()),
            ('change', self.gf('django.db.models.fields.TextField')()),
            ('motivate', self.gf('django.db.models.fields.TextField')()),
            ('creative', self.gf('django.db.models.fields.TextField')()),
            ('additional', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'awards', ['MostValuableCampaign'])

    def backwards(self, orm):
        # Deleting model 'MostValuableOrganizer'
        db.delete_table(u'awards_mostvaluableorganizer')

        # Deleting model 'MostValuableTechnology'
        db.delete_table(u'awards_mostvaluabletechnology')

        # Deleting model 'MostValuableCampaign'
        db.delete_table(u'awards_mostvaluablecampaign')


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
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
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
        u'awards.mostvaluablecampaign': {
            'Meta': {'object_name': 'MostValuableCampaign'},
            'additional': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'change': ('django.db.models.fields.TextField', [], {}),
            'contacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creative': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'innovation': ('django.db.models.fields.TextField', [], {}),
            'motivate': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'nominator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluablecampaign_nominees'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mvc_nominations'", 'to': u"orm['%s']" % organization_orm_label}),
            'personal_statement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluablecampaign_nominations'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('unconference',)", 'max_length': '50', 'populate_from': "'name'"}),
            'unconference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Unconference']"})
        },
        u'awards.mostvaluableorganizer': {
            'Meta': {'object_name': 'MostValuableOrganizer'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'courage': ('django.db.models.fields.TextField', [], {}),
            'excellence': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'innovation': ('django.db.models.fields.TextField', [], {}),
            'nominator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluableorganizer_nominees'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'personal_statement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluableorganizer_nominations'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'respect': ('django.db.models.fields.TextField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('unconference',)", 'max_length': '50', 'populate_from': "'profile'"}),
            'unconference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Unconference']"})
        },
        u'awards.mostvaluabletechnology': {
            'Meta': {'object_name': 'MostValuableTechnology'},
            'accessibility': ('django.db.models.fields.TextField', [], {}),
            'additional': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'innovation': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nominator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluabletechnology_nominees'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mvt_nominations'", 'to': u"orm['%s']" % organization_orm_label}),
            'personal_statement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'potential': ('django.db.models.fields.TextField', [], {}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mostvaluabletechnology_nominations'", 'to': u"orm['%s']" % user_profile_orm_label}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('unconference',)", 'max_length': '50', 'populate_from': "'name'"}),
            'unconference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Unconference']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        organization_model_label: {
            'Meta': {'object_name': Organization.__name__, 'db_table': "'%s'" % Organization._meta.db_table},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        user_profile_model_label: {
            'Meta': {'object_name': UserProfile.__name__, 'db_table': "'%s'" % UserProfile._meta.db_table},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'thewall.day': {
            'Meta': {'ordering': "('day', 'name')", 'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 9, 15, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thewall.participant': {
            'Meta': {'ordering': "('user__last_name', 'user__first_name')", 'object_name': 'Participant'},
            '_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'attendeenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['%s']" % user_orm_label, 'unique': 'True'})
        },
        u'thewall.unconference': {
            'Meta': {'object_name': 'Unconference'},
            'actionkit_page_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['thewall.Day']", 'symmetrical': 'False'}),
            'eventbrite_page_id': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['thewall.Participant']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '127'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thewall.Venue']"})
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

    complete_apps = ['awards']