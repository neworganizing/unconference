"""Decorators for Unconference Project"""

from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from functools import wraps

def render_to(template=None, mimetype="text/html", ajax=False):
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('template', template)
            ajax_please = output.pop('ajax', ajax)
            if ajax_please:
                if settings.DEBUG == True:
                    return HttpResponse(simplejson.dumps(output, indent=4), mimetype='text/javascript')
                else:
                    return HttpResponse(simplejson.dumps(output), mimetype='text/javascript')
            else:
                return render_to_response(tmpl, output, context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer