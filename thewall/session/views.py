from thewall.session.models import Session, Room, Venue, Slot, Day, SessionTag

from thewall.utility.decorators import render_to

@render_to("home.html")
def home(request):
    return { 'sessions': Session.objects.select_related().all() }