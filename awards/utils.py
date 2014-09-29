from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from actionkit import ActionKit

import logging
ak_logger = logging.getLogger('actionkit')

from django.shortcuts import render_to_response
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
                if settings.DEBUG:
                    return HttpResponse(
                        simplejson.dumps(
                            output, indent=4
                        ), mimetype='text/javascript'
                    )
                else:
                    return HttpResponse(
                        simplejson.dumps(output), mimetype='text/javascript'
                    )
            else:
                return render_to_response(
                    tmpl, output, context_instance=RequestContext(request),
                    mimetype=mimetype
                )
        return wrapper
    return renderer


def award_to_actionkit(page, award, form_data):
    action_prepended_data = dict(map(lambda (key, value): (
        "action_" + str(key), unicode(value)
    ), form_data.items()))

    # TODO: These need to be updated to reflect new data model
    extra_data = {
        'page': str(page),
        'action_award': str(award),
        'first_name': form_data['nominator_first_name'],
        'last_name': form_data['nominator_last_name'],
        'email': form_data['nominator_email'],
        'postal': '53211'
    }

    raw_akit_data = dict(extra_data.items() + action_prepended_data.items())
    akit_data = dict((k, v) for k, v in raw_akit_data.iteritems() if v)

    ak = ActionKit(
        instance=settings.AK_HOST,
        username=settings.AK_USER,
        password=settings.AK_PASS
    )

    ak_result = ak.action.create(akit_data)
    ak_logger.info(unicode(ak_result))


def get_user_profile_model_name():
    if hasattr(settings, "USER_PROFILE_MODEL"):
        try:
            app_label, model_name = settings.USER_PROFILE_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "USER_PROFILE_MODEL must be of the form 'app_label.model_name'"
            )

        return '%s.%s' % (app_label, model_name)
    else:
        raise ImproperlyConfigured(
            "You must specify USER_PROFILE_MODEL in settings.py"
        )


def get_user_profile_model():
    from django.db.models import get_model

    if hasattr(settings, "USER_PROFILE_MODEL"):
        try:
            app_label, model_name = settings.USER_PROFILE_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "USER_PROFILE_MODEL must be of the form 'app_label.model_name'"
            )

        user_profile_model = get_model(app_label, model_name)
        if user_profile_model is None:
            raise ImproperlyConfigured(
                """
                USER_PROFILE_MODEL refers to model '%s'
                that has not been installed
                """ % settings.USER_PROFILE_MODEL
            )
        return user_profile_model
    else:
        raise ImproperlyConfigured(
            "You must specify USER_PROFILE_MODEL in settings.py"
        )


def get_organization_model_name():
    if hasattr(settings, "ORGANIZATION_MODEL"):
        try:
            app_label, model_name = settings.ORGANIZATION_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "ORGANIZATION must be of the form 'app_label.model_name'"
            )

        return '%s.%s' % (app_label, model_name)
    else:
        raise ImproperlyConfigured(
            "You must specify ORGANIZATION in settings.py"
        )


def get_organization_model():
    from django.db.models import get_model

    if hasattr(settings, "ORGANIZATION_MODEL"):
        try:
            app_label, model_name = settings.ORGANIZATION_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "ORGANIZATION_MODEL must be of the form 'app_label.model_name'"
            )

        org_model = get_model(app_label, model_name)
        if org_model is None:
            raise ImproperlyConfigured(
                """
                USER_PROFILE_MODEL refers to model '%s' that
                has not been installed
                """ % settings.ORGANIZATION_MODEL)
        return org_model
    else:
        raise ImproperlyConfigured(
            "You must specify ORGANIZATION_MODEL in settings.py"
        )
