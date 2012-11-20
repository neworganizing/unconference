from django.conf.urls import patterns, include, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from thewall.session.models import Session

class MyResource(ModelResource):
	model = Session
	fields = {
	    'id',
	    'title',
	    'description',
	    'presenters',
	    'tags',
	    'slot',
	    'room',
	    'difficulty',
	    'created',
	    'modified',
	}

urlpatterns = patterns('',
	url(r'^restframework', include('djangorestframework.urls', namespace='djangorestframework')),
	url(r'^$', ListOrCreateModelView.as_view(resource=MyResource)),
	url(r'^(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=MyResource)),
)