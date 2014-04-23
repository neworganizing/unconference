"""Models for Session App"""

from django.db import models
from django.db.models import Sum
from django.contrib import admin
from django.conf import settings
import datetime

"""Models for Participants"""

class Participant(models.Model):
    """Presenter Information"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    #name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    attendeenumber = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        """Unicode representation of participant"""
        return self.user.first_name + " " + self.user.last_name + " (" + self.organization + ")"

"""Models for Sessions"""

class SessionTag(models.Model):
    """Session Tags"""
    tag = models.CharField(blank=False, max_length=20)

    class Admin(object):
        list_display = ('tag',)
        search_fields = ('tag',)

    def __unicode__(self):
        return self.tag

class Day(models.Model):
    """Day of Unconference"""
    name = models.CharField(max_length=100)
    day = models.DateField(default=datetime.datetime.today)

    class Admin(object):
        list_display = ('name',)

    def __unicode__(self):
        return self.name

    def day_slug(self):
        return "day-%s" % self.pk

class Slot(models.Model):
    """Timeslots"""
    day = models.ForeignKey(Day)
    name = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Admin(object):
        list_display = ('name', 'day')
        list_filter = ('day',)

    class Meta(object):
        ordering = ('day__day', 'start_time')

    def __unicode__(self):
        return self.day.name + " " + self.name + " (" + datetime.time.strftime(self.start_time,"%I:%M %p") + " - " + datetime.time.strftime(self.end_time,"%I:%M %p") + ")"

class Venue(models.Model):
    """Venue Location"""
    name = models.CharField(max_length=100)
    address1 = models.CharField(blank=True, max_length=100)
    address2 = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    """Room in the center"""
    name = models.CharField(max_length=100)
    floor = models.CharField(max_length=20)
    venue = models.ForeignKey(Venue)

    def __unicode__(self):
        return self.name


class Session(models.Model):
    """Actual Sessions"""
    title = models.TextField()
    description = models.TextField()
    headline = models.TextField()
    presenters = models.ManyToManyField(Participant)
    tags = models.ManyToManyField(SessionTag)
    slot = models.ForeignKey(Slot, null=True, blank=True)
    room = models.ForeignKey(Room, null=True, blank=True)
    difficulty = models.CharField(max_length=30, choices=(('B', 'Beginner'), ('I','Intermediate'), ('A','Advanced')), default='Beginner')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.title


    def vote_width(self):
        # votes / highest votes * 100
        annotated_sessions = Session.objects.annotate(total_votes=Sum('votes__value')).order_by('total_votes')
        for session in annotated_sessions:
            print session, session.total_votes
        highest_votes = annotated_sessions[0]
        print highest_votes, highest_votes.total_votes
        return (self.votes.count() / float(highest_votes.total_votes)) * 100.0

VALUES = (
    (u'+1', +1),
    (u'-1', -1)
)

class Vote(models.Model):
    session = models.ForeignKey(Session, related_name="votes")
    participant = models.ForeignKey(Participant, related_name="votes")
    value = models.SmallIntegerField(choices=VALUES)

    class Meta:
        unique_together = (('participant', 'session'),)

    def __unicode__(self):
        return u"{0} voted {1} on {2}".format(self.participant.user, self.value, self.session)

admin.site.register(Slot)
admin.site.register(Day)
admin.site.register(Room)
admin.site.register(Venue)
admin.site.register(SessionTag)
# Session?
# Participant?
# Vote?