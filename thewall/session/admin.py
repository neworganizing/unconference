from django.contrib import admin

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

from thewall.session.models import *
from thewall.participants.models import Participant

class SessionAdmin(AjaxSelectAdmin):
	form = make_ajax_form(Session, {'presenters': 'participant'})

admin.site.register(Session, SessionAdmin)