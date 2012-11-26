from django.http import Http404
from django.shortcuts import redirect, render_to_response

from thewall.session.models import Session, Room, Venue, Slot, Day, SessionTag

from thewall.utility.decorators import render_to

import datetime

@render_to()
def home(request):
    return { 
        'currentsessions': Session.objects.select_related().filter(slot__day__day__gte=datetime.datetime.today).order_by('slot__day','slot__start_time'),
        'pastsessions': Session.objects.select_related().filter(slot__day__day__lt=datetime.datetime.today).order_by('slot__day','slot__start_time'),
        'template': 'list.html'
    }


def filter(request):
    if request.method == 'GET':
        raise Http404

    return redirect("/%s/%s/" % (request.POST['time'],request.POST['room']))
