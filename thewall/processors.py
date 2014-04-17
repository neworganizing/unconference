"""Context processors for session lists"""

from thewall.session.models import *
from django.contrib.sites.models import get_current_site
from thewall.settings import GA_ID, GA_DOMAIN

def general(request):
    """General context info for app"""
    current_site = get_current_site(request)
    return {
        'sitename': current_site.name,
        'GA_ID': GA_ID,
        'GA_DOMAIN': GA_DOMAIN
    }

def session_times(request):
    """Session time information"""
    day = Day.objects.all().order_by('day')
    slots = Slot.objects.all().order_by('day__day','start_time')
    room = Room.objects.select_related().all().order_by('floor', 'name')
    tag = SessionTag.objects.all()
    return {
        'days': day,
        'slots': slots,
        'rooms': room,
        'tags': tag
    }
