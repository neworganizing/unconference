from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import logging
ak_logger = logging.getLogger('actionkit')


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
