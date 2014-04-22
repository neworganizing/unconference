"""Views for session app"""
import datetime
import time
import requests

from bs4 import BeautifulSoup

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import TemplateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from thewall.models import Session, Day, Slot, Venue, Room, Participant
from thewall.serializers import SessionSerializer
from thewall.forms import SessionForm
from thewall.decorators import render_to

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

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
    start_time = None

    if slot_start and slot_start != 'None':
        slot_start = time.strptime(slot_start, "%I:%M %p")
        start_time = time.strftime("%H:%M", slot_start)

    try:
        output['slot'] = Slot.objects.get(day=day, start_time=start_time)
    except Slot.DoesNotExist:

        if slot_start != 'None':
            slot_end = list(slot_start)
            slot_end[3] = (slot_end[3] + 1)%23
            slot_end = time.struct_time(tuple(slot_end))

            slot_end = time.strftime("%H:%M", slot_end)
            slot_start = time.strftime("%H:%M", slot_start)

            output['slot'] = Slot.objects.create(day=day,
                                       start_time=start_time,
                                       end_time=slot_end,
                                       name=''
            )
            output['slot'].save()
        else:
            output['slot'] = Slot.objects.create(day=day,
                start_time=None,
                end_time=None,
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
    if session_data['name']:
        output['title'] = session_data['name'].encode('utf-8')

    if session_data['headline']:
        output['headline'] = session_data['headline'].encode('utf-8')

    if session_data['description']:
        output['description'] = session_data['description'].encode('utf-8')

    return output

# Session filters
current_sessions_filter = (~Q(slot=None) & (Q(slot__day__day__gt=datetime.datetime.today) | (Q(slot__day__day=datetime.datetime.today) & Q(slot__start_time__gte=datetime.datetime.now))))
past_sessions_filter = (~Q(slot=None) & (Q(slot__day__day__lt=datetime.datetime.today) | (Q(slot__day__day=datetime.datetime.today) & Q(slot__start_time__lte=datetime.datetime.now))))

### VIEWS USING DJANGO GENERIC VIEWS ###

# Create participant for current user, or any user if staff
class CreateParticipantView(CreateView):
    pass

### CRAZY VIEW THAT DOES EVERYTHING BASE ON RAILS MODEL ###
class SessionView(TemplateView):
    get_actions = ['new', 'edit', 'show', 'index', 'delete']
    post_actions = ['create', 'update']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

        if not context['action']:
            if context['session']:
                    context['action'] = 'show'
            elif context['id']:
                context['action'] = context['id']
            else:
                context['action'] = 'index'

        if context['action'] in self.get_actions:
            return getattr(self, context['action'])(request, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

        if context.get('session', None):
            context['action'] = 'update'
        else:
            context['action'] = 'create'

        if context['action'] in self.post_actions:
            return getattr(self, context['action'])(request, context)


    def get_context_data(self, *args, **kwargs):
        context = super(SessionView, self).get_context_data(*args, **kwargs)
        context['id'] = kwargs.get('id', None)
        context['action'] = kwargs.get('action', None)

        if context['id']:
            try:
                context['session'] = get_object_or_404(Session, pk=context['id'])
            except ValueError:
                context['session'] = None
        else:
            context['sessions'] = Session.objects.all()

        return context

    @method_decorator(login_required(login_url='/users/login'))
    def index(self, request, context):
        context['view'] = self.request.GET.get('view', None)
        if context['view'] == 'schedule':
            context['currentsessions'] = Session.objects.select_related().filter(current_sessions_filter).order_by('slot__day','slot__start_time')
            context['pastsessions'] =  Session.objects.select_related().filter(past_sessions_filter).order_by('-slot__day','-slot__start_time')
            self.template_name = 'session/list.html'
        else:
            self.template_name = "session/index.html"
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/users/login'))
    def show(self, request, context):
        self.template_name = "session/show.html"
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/users/login'))
    def new(self, request, context):
        try:
            participant = self.request.user.participant
        except Participant.DoesNotExist:
            return HttpResponseRedirect('/participants/new')

        if not context.get('form', None):
            context['form'] = SessionForm(initial=dict(presenters=[self.request.user.participant,]))
        self.template_name = "session/new.html"
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/users/login'))
    def create(self, request, context):
        context['form'] = SessionForm(self.request.POST)

        if context['form'].is_valid():
            context['session'] = context['form'].save()
            return HttpResponseRedirect(
                reverse('session', kwargs={'id': context['session'].pk})
            )
        else:
            return self.new(context)

    @method_decorator(login_required(login_url='/users/login'))
    def edit(self, request, context):
        if not context.get('form', None):
            context['form'] = SessionForm(instance=context['session'])
        self.template_name = "session/edit.html"
        return self.render_to_response(context)


    @method_decorator(login_required(login_url='/users/login'))
    def update(self, request, context):
        context['form'] = SessionForm(self.request.POST, instance=context['session'])

        if context['form'].is_valid():
            context['session'] = context['form'].save()
            return HttpResponseRedirect(
                reverse('session', kwargs={'id': context['session'].pk})
            )
        else:
            return self.edit(context)

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
            except IndexError:
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