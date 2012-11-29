from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from eventbrite import EventbriteClient

from thewall.settings import EB_USERKEY, EB_APPKEY, EB_OAUTHKEY, EB_EVENTID

from thewall.participants.models import Participant

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
        if (EB_EVENTID == None):
            return "Sorry, no Eventbrite EventID has been found\nBe sure to add EB_EVENTID to your environment\n"

        if EB_USERKEY and EB_APPKEY:
            eb = EventbriteClient({'app_key': EB_APPKEY, 'user_key': EB_USERKEY})
        elif EB_OAUTHKEY:
            eb = EventbriteClient({'access_code': EB_OAUTHKEY})
        else:
            return "Sorry, No Eventbrite Access Methods Found\nBe sure to add EB_APPKEY and EB_USERKEY or EB_OAUTHKEY to your environment\n"


        # Grab all of our attendees
        print "Downloading Attendees from EventBrite"
        attendees = eb.event_list_attendees({'id': EB_EVENTID})['attendees']

        # Setup our counters
        handled = 0
        numcreated = 0

        # Loop over all our attendees
        print "Adding/Updating Attendee Database"
        for x in attendees:

            # EB returns a dictionary with all attendee data under 'attendee', lets just assign the value of that dictionary to a variable
            a = x['attendee']

            # Lets assemble our participant's name. We'll ignore unicode characters.
            name = '%s %s' % (a['first_name'].encode('ascii', 'ignore'), a['last_name'].encode('ascii', 'ignore'))

            # Check to see if there is a 'company' field returned, if so, save assign it to org
            if a.has_key('company'):
                org = a['company'].encode('ascii', 'ignore')
            else:
                org = 'Independent'

            # Check to see if the 'company' field we got back was blank. If so, set the participant's organization to 'Independent'
            if org == '':
                org = 'Independent'

            # Set our attendee number
            number = str(a['id'])

            # get_or_create is a nice helper function here. It will run a SELECT statement for each attendee, so it isn't optimal, but 2000 select queries won't kill the database
            obj, created = Participant.objects.get_or_create(attendeenumber=number, defaults={ 'name': name, 'organization': org })

            # As get_or_create returns a touple, lets test to see if a new object is created and increase our counter
            if created == True:
                numcreated += 1

            # Lets print out some basic information for the individual running the sync
            if options['list']:
                print '%s %s %s' % (name, org, number)
            handled += 1

        # Some final stats
        return("\n%i Attendees\n%i Added to Database\n" % (handled, numcreated))
