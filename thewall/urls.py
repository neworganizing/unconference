"""URLs for Unconference Project"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('thewall.api.urls')),
    url(r'^results/', 'thewall.session.views.results', name='results'),
    url(r'^filter', 'thewall.session.views.filter', name='filter'),
    #url(r'^refresh/', 'thewall.session.views.refresh', name='refresh'),
    url(r'^$', 'thewall.session.views.home', name='home'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
