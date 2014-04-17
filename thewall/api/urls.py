"""API Resources"""

from django.conf.urls import patterns, include, url
from rest_framework import routers
from thewall.session.models import Session

urlpatterns = patterns('',
    #url(r'^restframework', include('djangorestframework.urls', namespace='djangorestframework')),
    #url(r'^$', ListModelView.as_view(resource=MyResource)),
    #url(r'^(?P<pk>[^/]+)/$', ListModelView.as_view(resource=MyResource)),
)
