from rest_framework import serializers

from thewall.session.models import Session

class SessionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
	    model = Session
	    fields = (
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
	    )