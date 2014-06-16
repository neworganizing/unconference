from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from optparse import make_option
from eventbrite import EventbriteClient

from thewall.models import Participant, Unconference

User = get_user_model()

class Command(BaseCommand):
    """Pull all the attendees from Eventbrite"""
    help = "Pull all attendees from Eventbrite"

    option_list = BaseCommand.option_list + (
        make_option('--list',
            '-l',
            action='store_true',
            dest='list',
            default=False,
            help='List all attendees'),
    )

    def handle(self, *args, **options):
        # Try to start a connection with eventbrite, this will work with both the EventBrite OAuth2 method and a app/user key
        # We test on App/User method though

        events = Unconference.objects.all()

        if hasattr(settings, "EB_USERKEY") and hasattr(settings, "EB_APPKEY"):
            eb = EventbriteClient({'app_key': settings.EB_APPKEY, 'user_key': settings.EB_USERKEY})
        elif hasattr(settings, "EB_OAUTHKEY"):
            eb = EventbriteClient({'access_code': settings.EB_OAUTHKEY})
        else:
            return "Sorry, No Eventbrite Access Methods Found\nBe sure to add EB_APPKEY and EB_USERKEY or EB_OAUTHKEY to your environment\n"

        results = []

        for event in events:
            results.append(pull_attendees_for_event(eb, event, options))

        return "\n".join(results)

def pull_attendees_for_event(eb, event, options={}):
        if not event.eventbrite_page_id:
            return "Sorry, there is no eventbrite event id for this event."

        # Grab all of our attendees
        print "Downloading Attendees from EventBrite for ", event.name

        attendees = eb.event_list_attendees({'id': event.eventbrite_page_id})['attendees']

        # Setup our counters
        handled = 0
        numcreated = 0

        # Loop over all our attendees
        print "Adding/Updating Attendee Database"
        for person in attendees:

            # EB returns a dictionary with all attendee data under 'attendee', lets just assign the value of that dictionary to a variable
            a = person['attendee']

            # Lets assemble our participant's name. We'll ignore unicode characters.
            first_name = a['first_name'].encode('ascii', 'ignore')
            last_name = a['last_name'].encode('ascii', 'ignore')
            number = str(a['id'])
            email = a['email'].encode('ascii', 'ignore')

            # User must have email address
            if not email:
                continue

            # Check to see if there is a 'company' field returned, if so, save assign it to org
            org = a.get('company', 'Independent').encode('ascii', 'ignore')

            # Check to see if the 'company' field we got back was blank. If so, set the participant's organization to 'Independent'
            if not org:
                org = 'Independent'

            # First, find user
            user, user_created = User.objects.get_or_create(email=email)
        
            password = None

            if not user.first_name:
                user.first_name = first_name
            if not user.last_name:
                user.last_name = last_name

            print "Password: ", user.password
            if not user.has_usable_password():
                password = '{0}{1}'.format(first_name[0].lower(), last_name.lower())
                user.set_password(password)

            user.save()

            if not user_created:
                print "User: {0} {1} exists.".format(first_name, last_name)

            participant, participant_created = Participant.objects.get_or_create(user=user)
            participant.attendeenumber = number
            if not participant.organization:
                participant.organization = org
            participant.save()

            if not event.participants.filter(pk=participant.pk).exists():
                print "Adding user {0} to event {1}".format(user, event)
                event.participants.add(participant)

                # Email participant info about the event
                to = user.email
                from_email = 'Rootscamp Moderator <data@neworganizing.com>'
                domain = settings.DOMAIN
                    
                subject = u"Submit session ideas for {0}".format(event)
                    
                if user_created:
                    html = render_to_string("session/email/new_attendee_added.html", {"user": user, "domain": domain, "event": event, "password": password})
                else:
                    html = render_to_string("session/email/existing_attendee_added.html", {"user": user, "domain": domain, "event": event})

                text = strip_tags(html)

                msg = EmailMultiAlternatives(subject, text, from_email, [to])
                msg.attach_alternative(html, "text/html")

                try:
                    msg.send()
                except:
                    pass



            # As get_or_create returns a touple, lets test to see if a new object is created and increase our counter
            if user_created == True:
                numcreated += 1

            # Lets print out some basic information for the individual running the sync
            if options.get('list', False):
                print '%s %s %s %s %s' % (first_name, last_name, email, org, number)

            handled += 1

        event.save()

        # Some final stats
        return("\n%i Attendees\n%i Added to Database\n" % (handled, numcreated))