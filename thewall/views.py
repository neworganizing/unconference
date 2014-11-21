"""Views for session app"""
import datetime
import time
import requests
import json

from bs4 import BeautifulSoup

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.conf import settings
from django.views.generic import (View, TemplateView, CreateView, UpdateView,
                                  ListView)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.contrib import messages

from rest_framework import viewsets

from thewall.models import (Session, Day, Slot, Venue, Room, Participant,
                            Vote, SessionTag, Unconference)
from thewall.serializers import SessionSerializer
from thewall.forms import (SessionForm, SessionScheduleForm,
                           CreateParticipantForm, ParticipantForm)
from thewall.decorators import render_to

User = get_user_model()


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

# designed for ajax
# pattern is r'^sessions/(?P<id>[0-9]+)/vote/?$'


class VoteView(View):
    def post(self, request, *args, **kwargs):
        try:
            participant = request.user.participant
        except Participant.DoesNotExist:
            participant = Participant(user=request.user)
            participant.save()

        session_id = kwargs.get('id', None)
        unconf = kwargs.get('unconf', None)
        value = request.POST.get('value', None)

        if session_id and value:
            vote, created = Vote.objects.get_or_create(
                participant=participant,
                session_id=session_id
            )
            vote.value = value
            vote.save()

        session = Session.objects.get(unconference__slug=unconf, pk=session_id)
        response_data = dict(
            vote_width=session.vote_width(),
            session_id=session.pk
        )

        # no response data is necessary
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# ## VIEWS USING DJANGO GENERIC VIEWS ## #

class UnconferencesView(ListView):
    template_name = "unconferences.html"
    model = Unconference
    queryset = Unconference.objects.order_by('-days__day')

# Create participant for current user


class CreateUserView(CreateView):
    form_class = ParticipantForm

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)

        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            account_url = reverse("update_participant")
            next_url = reverse(
                "session",
                kwargs={
                    "unconf": request.POST.get('unconf', None)
                }
            )

            messages.info(
                request,
                """
                Your account has been created! <a href="{0}?next={1}">Add a password</a> to login again later.
                """.format(account_url, next_url)
            )
            return HttpResponseRedirect(
                reverse(
                    'session',
                    kwargs={
                        'unconf': request.POST.get('unconf', None)
                    }
                )
            )
        else:

            if 'email' in form.errors:
                user = get_user_model().objects.get(
                    email=request.POST.get('email', None)
                )

                if user.has_usable_password():
                    messages.info(
                        request,
                        """
                        This email address is already registered,
                        please login.
                        """
                    )

                    next_url = reverse(
                        'session',
                        kwargs={
                            'unconf': request.POST.get('unconf', None)
                        }
                    )

                    return HttpResponseRedirect(
                        settings.LOGIN_URL+"?next={0}".format(next_url)
                    )
                else:

                    account_url = reverse("update_participant")
                    next_url = reverse(
                        "session",
                        kwargs={
                            "unconf": request.POST.get('unconf', None)
                        }
                    )
                    messages.info(
                        request,
                        """
                        Found your account! <a href="{0}?next={1}">Add a password</a> to login again later.
                        """.format(account_url, next_url)
                    )
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
            else:
                messages.error(
                    request,
                    """
                    Failed to create account!  Please try again. Errors: {0}
                    """.format(form.errors)
                )

            return HttpResponseRedirect(
                reverse(
                    'session',
                    kwargs={
                        'unconf': request.POST.get('unconf', None)
                    }
                )
            )


class CreateParticipantView(CreateView):
    form_class = CreateParticipantForm
    template_name = "participant/form.html"

    @method_decorator(login_required(login_url='/users/login'))
    def get(self, request, *args, **kwargs):
        return super(CreateParticipantView, self).get(
            request, *args, **kwargs
        )

    @method_decorator(login_required(login_url='/users/login'))
    def post(self, request, *args, **kwargs):
        return super(CreateParticipantView, self).post(
            request, *args, **kwargs
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateParticipantView, self).form_valid(form)

    def get_success_url(self):
        success_url = self.request.POST.get(
            'next', None
        )
        return success_url

    def get_context_data(self, *args, **kwargs):
        context = super(CreateParticipantView, self).get_context_data(
            *args, **kwargs
        )

        context['unconf'] = kwargs.get('unconf', None)
        context['next'] = self.request.GET.get(
            'next', reverse("session", kwargs={"unconf": context['unconf']})
        )

        return context


class UpdateParticipantView(UpdateView):
    form_class = CreateParticipantForm
    # user_form_class = UserChangeForm
    template_name = "participant/form.html"

    @method_decorator(login_required(login_url='/users/login'))
    def get(self, request, *args, **kwargs):
        return super(UpdateParticipantView, self).get(request, *args, **kwargs)

    @method_decorator(login_required(login_url='/users/login'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        # user_form = self.user_form_class(request.POST)

        if form.is_valid():  # and user_form.is_valid():
            form.save()
            # user_form.save()
            messages.info(request, 'User information updated successfully.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data(*args, **kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        success_url = self.request.POST.get(
            'next', '/'
        )
        return success_url

    def get_object(self, queryset=None):
        try:
            self.object = self.request.user.participant
        except Participant.DoesNotExist:
            self.object = Participant(user=self.request.user)
            self.object.save()

        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateParticipantView, self).get_context_data(
            *args, **kwargs
        )
        context['unconf'] = kwargs.get('unconf', None)
        context['next'] = self.request.GET.get(
            'next', '/'
        )
        # if 'user_form' not in context:
        #    context['user_form'] = UserChangeForm(instance=self.request.user)
        return context

#  ## CRAZY VIEW THAT DOES EVERYTHING BASED ON RAILS' MODEL ##  #


class SessionView(TemplateView):
    get_actions = ['new', 'edit', 'show', 'index', 'delete']
    post_actions = ['create', 'update']

    # @method_decorator(login_required(login_url='/users/login'))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

#        if not request.user.is_authenticated():
#            context['user_form'] = ParticipantForm()

        if not context['action']:
            if context.get('session', None):
                    context['action'] = 'show'
            elif context['id']:
                context['action'] = context['id']
            else:
                context['action'] = 'index'

        if context['action'] in self.get_actions:
            return getattr(self, context['action'])(request, context)

    # @method_decorator(login_required(login_url='/users/login'))
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
        context['unconf'] = kwargs.get('unconf', None)
        # unconference = Unconference.objects.get(slug=context['unconf'])

        # Hack to allow testers to mess with one conference,
        # but otherwise only participants can see it
        #if unconference.slug != 'testcamp':
        #    try:
        #        participant = self.request.user.participant
        #    except Participant.DoesNotExist:
        #        raise Http404

        #    if not participant in unconference.participants.all():
        #        raise Http404

        if not context['unconf']:
            return Http404

        if context['id']:
            try:
                context['session'] = get_object_or_404(
                    Session, unconference__slug=context['unconf'],
                    pk=context['id']
                )
            except ValueError:
                context['session'] = None
        else:  # A listing of all sessions, check for filters
            time = self.request.GET.get("time", "all")
            tag = self.request.GET.get("tag", "all")
            room = self.request.GET.get("room", "all")

            filter = dict()

            if time != "all":
                filter_param = time.split('-')
                context['time_id'] = time
                if filter_param[0] == 'day':
                    filter['slot__day'] = filter_param[1]
                else:
                    filter['slot'] = time

            if tag != "all":
                context['tag_id'] = filter['tags__pk'] = tag

            if room != "all":
                context['room_id'] = filter['room'] = room

            filter['unconference__slug'] = context['unconf']

            context['sessions'] = Session.objects.filter(
                **filter
            ).select_related()

        return context

    # @method_decorator(login_required(login_url='/users/login'))
    def index(self, request, context):
        context['view'] = self.request.GET.get('view', None)

        if context['view'] == 'schedule':
            context['days'] = Day.objects.filter(
                unconference__slug=context['unconf']
            )
            context['slots'] = Slot.objects.filter(day__in=context['days'])
            context['tags'] = SessionTag.objects.all()
            context['rooms'] = Room.objects.filter(
                venue__unconference__slug=context['unconf']
            )
            context['currentsessions'] = context['sessions'].filter(
                current_sessions_filter
            ).order_by(
                'slot__day', 'slot__start_time'
            )

            context['pastsessions'] = context['sessions'].filter(
                past_sessions_filter
            ).order_by(
                '-slot__day', '-slot__start_time'
            )
            self.template_name = 'session/list.html'

        elif context['view'] == 'wall':
            context['days'] = Day.objects.filter(
                unconference__slug=context['unconf']
            )
            context['rooms'] = Room.objects.filter(
                venue__unconference__slug=context['unconf']
            )
            slots = Slot.objects.filter(day__in=context['days'])

            # Construct wall
            context['wall'] = list()

            for slot in slots:
                row = dict()
                row['slot'] = slot
                row['rooms'] = dict()

                for room in context['rooms']:
                    row['rooms'][room.name] = None

                for session in slot.session_set.filter(
                    unconference__slug=context['unconf']
                ):
                    row['rooms'][session.room.name] = session

                row['rooms'] = sorted(row['rooms'].iteritems())

                context['wall'].append(row)

            self.template_name = 'session/wall.html'

        else:
            context['sessions'] = context['sessions'].annotate(
                total_votes=Sum('votes__value')
            ).order_by('-total_votes')
            self.template_name = "session/index.html"
        return self.render_to_response(context)

    # @method_decorator(login_required(login_url='/users/login'))
    def show(self, request, context):
        self.template_name = "session/show.html"
        return self.render_to_response(context)

    # @method_decorator(login_required(login_url='/users/login'))
    def new(self, request, context):
        # try:
        #    participant = self.request.user.participant
        # except Participant.DoesNotExist:
        #    return HttpResponseRedirect(
        #        reverse(
        #            'create_participant'
        #        )+'?next='+reverse("session",
        #            kwargs={"unconf": context['unconf'], "id": "new"})
        #        )

        if not context.get('form', None):
            initial = dict(
                unconference=Unconference.objects.get(slug=context['unconf'])
            )

            # if hasattr(request.user, 'participant'):
            #    presenters=[request.user.participant,],

            context['form'] = SessionForm(initial=initial)

        if not request.user.is_authenticated():
            if not context.get('participant_form', None):
                context['participant_form'] = ParticipantForm(
                    prefix='participant'
                )
            if not context.get('participant_details_form', None):
                context['participant_details_form'] = CreateParticipantForm(
                    prefix='participant_details'
                )

        self.template_name = "session/new.html"
        return self.render_to_response(context)

    # @method_decorator(login_required(login_url='/users/login'))
    def create(self, request, context):
        context['form'] = SessionForm(self.request.POST)
        context['participant_form'] = ParticipantForm(self.request.POST, prefix='participant')
        context['participant_details_form'] = CreateParticipantForm(self.request.POST, prefix='participant_details')

        user = None
        if context['form'].is_valid():
            if not request.user.is_authenticated():
                if context['participant_form'].is_valid() and context['participant_details_form'].is_valid():
                    user = context['participant_form'].save()
                    participant = context['participant_details_form'].save(commit=False)
                    participant.user = user
                    participant.save()
                    unconf = Unconference.objects.get(slug=context['unconf'])
                    unconf.participants.add(participant)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    messages.info(request,
                        """
                        Your account has been created!  To add a password, which is required to login later,
                        please click the <a href="/{% url "update_patricipants" %}?next={% url "session" unconf=unconf %}>"edit"</a> link next to your email at the top right of the page.
                        """
                    )
                else:
                    return self.new(request, context)
            else:
                user = request.user

            context['session'] = context['form'].save()
            #context['session'].presenters.add(request.user.participant)
            context['session'].creator = user
            context['session'].save()

            return HttpResponseRedirect(
                reverse('session', kwargs={'unconf': context['unconf']})
            )
        else:
            return self.new(request, context)

    @method_decorator(login_required(login_url='/users/login'))
    def edit(self, request, context):
        if (not (request.user.is_staff or \
            request.user.participant in context['session'].presenters.all())) \
            and request.user != context['session'].creator:
            raise Http404

        if not context.get('form', None):
            if request.user.is_staff:
                context['form'] = SessionScheduleForm(instance=context['session'])
            else:
                context['form'] = SessionForm(instance=context['session'])
        self.template_name = "session/edit.html"
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/users/login'))
    def update(self, request, context):
        if (not (request.user.is_staff or \
            request.user.participant in context['session'].presenters.all())) \
            and request.user != context['session'].creator:
            raise Http404

        if request.user.is_staff:
            context['form'] = SessionScheduleForm(self.request.POST, instance=context['session'])
        else:    
            context['form'] = SessionForm(self.request.POST, instance=context['session'])

        if context['form'].is_valid():
            context['session'] = context['form'].save()
            return HttpResponseRedirect(
                reverse('session', kwargs={"unconf": context['unconf']})
            )
        else:
            return self.edit(request,   context)

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
