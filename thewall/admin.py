"""Admin functionality for session app"""

from django.contrib import admin
from django.forms import SelectMultiple

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

from thewall.models import *


class ParticipantAdmin(admin.ModelAdmin):
    """Admin area for managing participants"""
    list_display = ('user', 'organization', 'attendeenumber')
    search_fields = ('user', 'user__email', 'attendeenumber')

admin.site.register(Participant, ParticipantAdmin)


class SessionAdmin(AjaxSelectAdmin):
    list_filter = ('slot', 'tags', 'room',)
    list_display = ('title', 'unconference', 'room', 'slot', 'description')
    search_fields = ('title',)

    form = make_ajax_form(Session, {'presenters': 'participant'})
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': SelectMultiple(attrs={'size': '15'})
        }
    }

admin.site.register(Session, SessionAdmin)


class UnconferenceAdmin(admin.ModelAdmin):
    pass


class SponsorshipAdmin(admin.ModelAdmin):
    list_filter = ('unconference', )
    list_display = ('organization', 'unconference', 'amount')
    search_fields = ('organization', )

admin.site.register(Unconference, UnconferenceAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
