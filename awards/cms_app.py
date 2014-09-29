from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class AwardsApphook(CMSApp):
    name = _("Awards App")
    urls = ["awards.urls"]

apphook_pool.register(AwardsApphook)
