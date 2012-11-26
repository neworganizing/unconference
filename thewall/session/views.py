from django.http import Http404
from django.shortcuts import redirect

from thewall.session.models import Session, Room, Venue, Slot, Day, SessionTag

from thewall.utility.decorators import render_to

@render_to("home.html")
def home(request):
    return { 'sessions': Session.objects.select_related().all() }

def filter(request):
    if request.method == 'GET':
        raise Http404

    return redirect("/%s/%s/" % (request.POST['time'],request.POST['room']))
