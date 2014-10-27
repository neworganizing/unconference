from django.db import models

from cms.models.pluginmodel import CMSPlugin

from thewall.models import Unconference


class SponsorPlugin(CMSPlugin):
    """
    Allows the unconference to use when displaying sponsorships
    """
    unconference = models.ForeignKey(Unconference)
