"""URLs for Unconference Project"""

from django.conf.urls import patterns, include, url
#from django.contrib import admin
#from django.conf import settings

from ajax_select import urls as ajax_select_urls
from rest_framework import routers

from thewall import views

#admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = patterns('',
	url(r'^lookups/', include(ajax_select_urls)),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^participants/new/?$', views.CreateParticipantView.as_view(), name='create_participant'),
    url(r'^participants/edit/?$', views.UpdateParticipantView.as_view(), name='update_participant'),
    url(r'^(?P<unconf>[a-zA-Z0-9]+)/sessions/?$', views.SessionView.as_view(), name='session'),
    url(r'^(?P<unconf>[a-zA-Z0-9]+)/sessions/(?P<id>[0-9]+)/vote/?$', views.VoteView.as_view(), name='vote'),
    url(r'^(?P<unconf>[a-zA-Z0-9]+)/sessions/(?P<id>[0-9]+)/(?P<action>[a-zA-Z]+)/?$', views.SessionView.as_view(), name='session'),
    url(r'^(?P<unconf>[a-zA-Z0-9]+)/sessions/(?P<id>[0-9a-zA-Z]+)/?$', views.SessionView.as_view(), name='session'),
    #url(r'^results$', views.results, name='results'),
    #url(r'^filter$', views.filter, name='filter'),
    #url(r'^refresh/', 'thewall.session.views.refresh', name='refresh'),
)

#if settings.DEBUG:
#    urlpatterns += patterns('django.contrib.staticfiles.views',
#        url(r'^static/(?P<path>.*)$', 'serve'),
#    )
