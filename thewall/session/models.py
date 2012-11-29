from django.db import models
from django.contrib import admin
from thewall.participants.models import Participant
import datetime

class SessionTag(models.Model):
	"""Session Tags"""
	tag = models.CharField(blank=False, max_length=20)

	class Admin:
		list_display = ('tag',)
		search_fields = ('tag',)

	def __unicode__(self):
		return self.tag

class Day(models.Model):
	"""Day of Unconference"""
	name = models.CharField(max_length=100)
	day = models.DateField(default=datetime.datetime.today)

	class Admin:
		list_display = ('name',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name


class Slot(models.Model):
	"""Timeslots"""
	day = models.ForeignKey(Day)
	name = models.CharField(max_length=10)
	start_time = models.TimeField()
	end_time = models.TimeField()

	class Admin:
		list_display = ('name','day')
		list_filter = ('day')
		search_fields = ('',)

	def __unicode__(self):
		return "Day: " + self.day.name + " Session: " + self.name

class Venue(models.Model):
	"""Venue Location"""
	name = models.CharField(max_length=100)
	address1 = models.CharField(blank=True, max_length=100)
	address2 = models.CharField(blank=True, max_length=100)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	postal = models.CharField(blank=True, max_length=100)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name


class Room(models.Model):
	"""Room in the center"""
	name = models.CharField(max_length=100)
	floor = models.CharField(max_length=20)
	venue = models.ForeignKey(Venue)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name + " in " + self.venue.name


class Session(models.Model):
	"""Actual Sessions"""
	title = models.CharField(max_length=120)
	description = models.TextField()
	presenters = models.ManyToManyField(Participant)
	tags = models.ManyToManyField(SessionTag)
	slot = models.ForeignKey(Slot)
	room = models.ForeignKey(Room)
	difficulty = models.CharField(max_length=30,choices=(('B', 'Beginner'),('I','Intermediate'),('A','Advanced')),default='Beginner')
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, auto_now_add=True)

	#class Admin:
	#	list_display = ('',)
	#	search_fields = ('',)

	def __unicode__(self):
		return self.title


admin.site.register(Slot)
admin.site.register(Day)
admin.site.register(Room)
admin.site.register(Venue)
admin.site.register(SessionTag)
#admin.site.register(Session)