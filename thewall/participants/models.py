from django.db import models
from django.contrib import admin

class Participant(models.Model):
	"""Presenter Information"""
	name = models.CharField(max_length=100)
	organization = models.CharField(max_length=100)
	attendeenumber = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.name + " (" + self.organization + ")"