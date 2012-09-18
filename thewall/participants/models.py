from django.db import models
from django.contrib import admin

class Organization(models.Model):
	"""Organization that presenter is part of"""
	name = models.CharField(max_length=100)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name

class Participant(models.Model):
	"""Presenter Information"""
	name = models.CharField(max_length=100)
	organization = models.ForeignKey(Organization)
	attendeenumber = models.IntegerField(blank=True, null=True)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name + " (" + self.organization.name + ")"

admin.site.register(Organization)
admin.site.register(Participant)