from django.contrib import admin

from thewall.participants.models import Participant

class ParticipantAdmin(admin.ModelAdmin):
        list_display = ('name','organization','attendeenumber',)
        search_fields = ('name','attendeenumber',)

admin.site.register(Participant,ParticipantAdmin)