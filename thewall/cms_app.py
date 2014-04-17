from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class WallApphook(CMSApp):
    name = _("Wall App")
    urls = ["thewall.urls"]

apphook_pool.register(WallApphook)