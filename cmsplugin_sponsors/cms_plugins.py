from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SponsorPlugin
from thewall.models import Sponsorship


class SponsorsPlugin(CMSPluginBase):
    model = SponsorPlugin
    name = _("Sponorship Plugin")
    render_template = "cmsplugin_sponsors/sponsors_plugin.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['sponsorships'] = Sponsorship.objects.filter(
            unconference=instance.unconference
        ).order_by('-amount', 'organization__name')
        return context

plugin_pool.register_plugin(SponsorsPlugin)
