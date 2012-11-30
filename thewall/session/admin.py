from django.contrib import admin
from django.forms import SelectMultiple

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

from thewall.session.models import *
from thewall.participants.models import Participant

class SessionAdmin(AjaxSelectAdmin):
    list_filter = ('slot','tags','room',)
    list_display = ('title','room','slot','description',)
    search_fields = ('title','presenters__name',)

    form = make_ajax_form(Session, {'presenters': 'participant'})
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}, }

admin.site.register(Session, SessionAdmin)