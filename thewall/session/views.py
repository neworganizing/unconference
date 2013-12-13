"""Views for session app"""

from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from thewall.session.models import Session, Day, Slot, Venue, Room

from thewall.utility.decorators import render_to

import datetime
import time
import requests

from bs4 import BeautifulSoup

current_sessions_filter = (Q(slot__day__day__gt=datetime.datetime.today) | (Q(slot__day__day=datetime.datetime.today) & Q(slot__start_time__gte=datetime.datetime.now)))
past_sessions_filter = (Q(slot__day__day__lt=datetime.datetime.today) | (Q(slot__day__day=datetime.datetime.today) & Q(slot__start_time__lte=datetime.datetime.now)))

# Helper functions
def has_data_subevent_id_attr(tag):
    return tag.has_attr('data-subevent-id')

def extract_session(session_data):
    output = dict()

    # check if day exists, create if not
    date = str(session_data['date']).split('/')
    date.append(2013)
    date = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))

    try:
        day = Day.objects.get(day=date)
    except Day.DoesNotExist:
        day = Day.objects.create(day=date, name=date.strftime("%A"))
        day.save()

    # check if timeslot exists, create if not
    slot_start = str(session_data['time'])

    if slot_start:
        slot_start = time.strptime(slot_start, "%I:%M %p")

    try:
        output['slot'] = Slot.objects.get(day=day, start_time=time.strftime("%H:%M", slot_start))
    except Slot.DoesNotExist:
        slot_end = list(slot_start)
        slot_end[3] = (slot_end[3] + 1)%23
        slot_end = time.struct_time(tuple(slot_end))

        output['slot'] = Slot.objects.create(day=day,
                                   start_time=time.strftime("%H:%M", slot_start),
                                   end_time=time.strftime("%H:%M", slot_end),
                                   name=''
        )
        output['slot'].save()

    # check if room exists, create if not
    room_text = str(session_data['location'])

    try:
        output['room'] = Room.objects.get(name=room_text)
    except Room.DoesNotExist:
        venue = Venue.objects.get(name="Convention Center")
        output['room'] = Room.objects.create(name=room_text,floor='',venue=venue)
        output['room'].save()

    # create session
    output['title'] = session_data['name'].encode('utf-8')
    output['headline'] = session_data['headline'].encode('utf-8')

    if session_data['description']:
        output['description'] = session_data['description'].encode('utf-8')

    return output

# View functions
@render_to()
def home(request):

    return { 
        'currentsessions': Session.objects.select_related().filter(current_sessions_filter).order_by('slot__day','slot__start_time'),
        'pastsessions': Session.objects.select_related().filter(past_sessions_filter).order_by('-slot__day','-slot__start_time'),
        'template': 'list.html'
    }

def refresh(request):

    # Scan website, construct BS object representing current state
    url = 'https://www.smartcrowdz.com/roots13/schedule'

    smartcrowdz_bs = BeautifulSoup(requests.get(url).text)
    session_text = smartcrowdz_bs.find_all(has_data_subevent_id_attr)

    session_data = dict()

    for session_tag in session_text:
        id = session_tag.get('data-subevent-id', None)

        if(id):
            session_data[id] = dict()
            try:
                session_data[id]['date'] = list(session_tag.children)[1].contents[0]
            except (IndexError, AttributeError):
                session_data[id]['date'] = None

            try:
                session_data[id]['time'] = list(session_tag.children)[3].contents[0]
            except (IndexError, AttributeError):
                session_data[id]['time'] = None

            try:
                session_data[id]['name'] = session_tag.find('div', class_='activity-name').contents[0]
            except (IndexError, AttributeError):
                session_data[id]['name'] = None

            try:
                session_data[id]['headline'] = session_tag.find('div', class_='activity-headline').contents[0]
            except (IndexError, AttributeError):
                session_data[id]['headline'] = ''

            try:
                session_data[id]['location'] = session_tag.find('div', class_='schedule-location').contents[0]
            except (IndexError, AttributeError):
                session_data[id]['location'] = None

            # Get detail page
            session_url = 'https://www.smartcrowdz.com/roots13/schedule_detail/{0}'.format(id)

            try:
                session_detail_text = BeautifulSoup(requests.get(session_url).text, "lxml")
            except:
                raise

            session_detail_text = session_detail_text.find(id='sub-event-detail-body')

            if session_detail_text:
                session_detail_text = session_detail_text.p

                if session_detail_text:
                    session_detail_text = session_detail_text.contents[0]

            try:
                session_data[id]['description'] = session_detail_text
            except (IndexError, AttributeError):
                session_data[id]['description'] = None

    print session_data

    # Loop over existing sessions, removing matches from session data and removing sesssions
    # that no longer exist
    sessions = Session.objects.all()

    for session in sessions:
        if not str(session.pk) in session_data:
            # session not found, delete it
            session.delete()
        else:
            # session found, update it and remove from list
            fields = extract_session(session_data[str(session.pk)])
            session.update(**fields)
            del session_data[str(session.pk)]


    # Loop over remaining session data and create new sessions
    for key, session in session_data.iteritems():
        fields = extract_session(session)
        new_session, created = Session.objects.get_or_create(**fields)

        if created:
            new_session.save()


    return redirect(reverse('home'))

@render_to()
def results(request):
    if 'time' not in request.session:
        return redirect('/')

    context = dict(
        currentsessions = Session.objects.select_related().filter(current_sessions_filter).order_by('slot__day','slot__start_time'),
        pastsessions = Session.objects.select_related().filter(past_sessions_filter).order_by('-slot__day','-slot__start_time'),
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
