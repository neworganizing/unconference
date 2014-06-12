from __future__ import absolute_import

import datetime
from django.conf import settings
from celery import shared_task
from eventbrite import EventbriteClient

from .models import Unconference
from .management.commands.pullattendees import pull_attendees_for_event

@shared_task
def sync_with_eventbrite():
    synced_confs = []

    if hasattr(settings, "EB_USERKEY") and hasattr(settings, "EB_APPKEY"):
        eb = EventbriteClient({'app_key': settings.EB_APPKEY, 'user_key': settings.EB_USERKEY})
    elif hasattr(settings, "EB_OAUTHKEY"):
        eb = EventbriteClient({'access_code': settings.EB_OAUTHKEY})
    else:
        return "Sorry, No Eventbrite Access Methods Found\nBe sure to add EB_APPKEY and EB_USERKEY or EB_OAUTHKEY to your environment\n"

    for conf in Unconference.objects.filter(days__day__gt=datetime.datetime.today()).distinct():
        synced_confs.append(pull_attendees_for_event(eb, conf))

    return synced_confs