from django import forms
from thewall.models import Session

class SessionForm(forms.ModelForm):

	class Meta:
		model = Session
		fields = ('title', 'description', 'headline', 'presenters', 'tags', 'difficulty')
		widgets = {"title": forms.TextInput(), 'headline': forms.TextInput()}

class SessionScheduleForm(forms.ModelForm):
	class Meta:
		model = Session
		fields = ('title', 'description', 'headline',
				  'presenters', 'tags', 'difficulty',
				  'slot', 'room')
		widgets = {"title": forms.TextInput(), 'headline': forms.TextInput()}	