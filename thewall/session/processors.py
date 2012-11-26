from thewall.session.models import *
from django.contrib.sites.models import get_current_site

def general(request):
    current_site = get_current_site(request)
    return {'sitename': current_site.name}

def session_times(request):
    # Return all available session days, slots and rooms
    day = Day.objects.all().order_by('day')
    slots = Slot.objects.all().order_by('day__day','start_time')
    room = Room.objects.select_related().all().order_by('floor','name')
    return {'days': day, 'slots': slots, 'rooms': room}