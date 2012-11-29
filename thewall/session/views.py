from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse

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

@render_to()
def results(request):
    if 'time' not in request.session:
        return redirect('/')

    context = dict(
        currentsessions = Session.objects.select_related().filter(slot__day__day__gte=datetime.datetime.today).order_by('slot__day','slot__start_time'),
        pastsessions = Session.objects.select_related().filter(slot__day__day__lt=datetime.datetime.today).order_by('slot__day','slot__start_time'),
        time_id = request.session['time'],
        tag_id = request.session['tag'],
        room_id = request.session['room'],
        template = 'list.html'
    )

    time = request.session.get('time', None)
    if time and time != 'all':        
        if time.split('-')[0] == 'day':
            day = time.split('-')[-1]

            context['currentsessions'] = context['currentsessions'].filter(slot__day=day)
            context['pastsessions'] = context['pastsessions'].filter(slot__day=day)
        else:
            context['currentsessions'] = context['currentsessions'].filter(slot=time)
            context['pastsessions'] = context['pastsessions'].filter(slot=time)

    tag = request.session.get('tag', None)
    if tag and tag != 'all':
        context['currentsessions'] = context['currentsessions'].filter(tags=tag)
        context['pastsessions'] = context['pastsessions'].filter(tags=tag)        


    room = request.session.get('room', None)
    if room and room != 'all':
        context['currentsessions'] = context['currentsessions'].filter(room=room)
        context['pastsessions'] = context['pastsessions'].filter(room=room)

    return context

def filter(request):
    if not request.POST['time']:
        raise Http404

    request.session['time'] = request.POST['time']
    request.session['tag'] = request.POST['tag']
    request.session['room'] = request.POST['room']

    return redirect(reverse('results'))
