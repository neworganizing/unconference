import datetime

from django.db import models
from django.db.models import Sum
from django.contrib import admin
from django.conf import settings

from .utils import get_organization_model_name

organization_model_name = get_organization_model_name()


class Participant(models.Model):
    """Presenter Information"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    attendeenumber = models.IntegerField(blank=True, null=True)
    _phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ('user__last_name', 'user__first_name', )

    def __unicode__(self):
        """Unicode representation of participant"""
        return self.user.first_name + " " + self.user.last_name + " (" + \
            self.organization + ")"

    def get_up_votes(self):
        if not hasattr(self, '_up_votes'):
            self._up_votes = self.votes.filter(
                value=1).values_list('session_id', flat=True)
        return self._up_votes

    def get_down_votes(self):
        if not hasattr(self, '_down_votes'):
            self._down_votes = self.votes.filter(
                value=-1).values_list('session_id', flat=True)
        return self._down_votes

    @property
    def phone(self):
        try:
            if hasattr(self.user, 'phone'):
                return self.user.phone
        except:
            pass

        return self._phone

    @phone.setter
    def phone(self, value):
        try:
            if self.user and hasattr(self.user, 'phone'):
                self.user.phone = value
                self.user.save()
                return
        except:
            pass

        self._phone = value

"""Models for Sessions"""


class SessionTag(models.Model):
    """Session Tags"""
    tag = models.CharField(blank=False, max_length=20)

    class Meta:
        ordering = ('tag',)

    class Admin(object):
        list_display = ('tag',)
        search_fields = ('tag',)

    def __unicode__(self):
        return self.tag.capitalize()


class Day(models.Model):
    """Day of Unconference"""
    name = models.CharField(max_length=100)
    day = models.DateField(default=datetime.datetime.today)

    class Meta:
        ordering = ('day', 'name',)
        get_latest_by = 'day'

    class Admin(object):
        list_display = ('name',)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.day)

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
        return self.day.name + " " + self.name + " (" + \
            datetime.time.strftime(
                self.start_time, "%I:%M %p"
            ) + " - " + datetime.time.strftime(self.end_time, "%I:%M %p") + ")"

    def time(self):
        return datetime.time.strftime(
            self.start_time, "%I:%M %p"
        ) + " - " + datetime.time.strftime(self.end_time, "%I:%M %p")


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

    class Meta:
        ordering = ('venue', 'name',)

    def __unicode__(self):
        return self.name


class Unconference(models.Model):
    slug = models.SlugField(max_length=127)
    name = models.CharField(max_length=127)
    venue = models.ForeignKey(Venue)
    days = models.ManyToManyField(Day)
    participants = models.ManyToManyField(Participant, blank=True)
    eventbrite_page_id = models.CharField(max_length=31, null=True, blank=True)
    actionkit_page_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class Session(models.Model):
    """Actual Sessions"""
    unconference = models.ForeignKey(Unconference, null=True, blank=True)
    title = models.TextField()
    description = models.TextField()
    headline = models.TextField()
    presenters = models.ManyToManyField(Participant, null=True, blank=True)
    tags = models.ManyToManyField(SessionTag)
    slot = models.ForeignKey(Slot, null=True, blank=True)
    room = models.ForeignKey(Room, null=True, blank=True)
    difficulty = models.CharField(
        max_length=30, choices=(
            ('B', 'Beginner'), ('I', 'Intermediate'), ('A', 'Advanced')
        ), default='Beginner'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True
    )
    extra_presenters = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = (('unconference', 'slot', 'room'),)
        ordering = ('title', )

    def vote_width(self):
        # votes / highest votes * 100
        annotated_sessions = Session.objects.filter(
            unconference=self.unconference
        ).annotate(total_votes=Sum('votes__value')).order_by('-total_votes')
        highest_votes = annotated_sessions[0]
        print highest_votes.total_votes
        if highest_votes.total_votes < 1:
            if self.total_vote() > 0:
                return 100
            else:
                return 0

        vote_width = (
            self.total_vote() / float(highest_votes.total_votes)
        ) * 100.0

        if vote_width < 0:
            vote_width = 0

        return vote_width

    def total_vote(self):
        if not hasattr(self, '_total_vote'):
            self._total_vote = self.votes.aggregate(Sum('value'))['value__sum']
        return self._total_vote

VALUES = (
    (u'0', 0),
    (u'+1', +1),
    (u'-1', -1)
)


class Vote(models.Model):
    session = models.ForeignKey(Session, related_name="votes")
    participant = models.ForeignKey(Participant, related_name="votes")
    value = models.SmallIntegerField(choices=VALUES, default=0)

    class Meta:
        unique_together = (('participant', 'session'),)

    def __unicode__(self):
        return u"{0} voted {1} on {2}".format(
            self.participant.user, self.value, self.session
        )


class Sponsorship(models.Model):
    organization = models.ForeignKey(organization_model_name)
    unconference = models.ForeignKey(Unconference)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return "{0}'s sponsorship of {1} at ${2}".format(
            self.organization,
            self.unconference,
            self.amount
        )

    class Meta:
        ordering = ['organization', 'unconference', 'amount']

admin.site.register(Slot)
admin.site.register(Day)
admin.site.register(Room)
admin.site.register(Venue)
admin.site.register(SessionTag)
