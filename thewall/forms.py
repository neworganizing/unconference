from django import forms
from thewall.models import Session

class NewSessionForm(forms.ModelForm):

	class Meta:
		model = Session
		fields = ('title', 'description', 'headline', 'presenters', 'tags', 'difficulty')
		widgets = {"title": forms.TextInput(), 'headline': forms.TextInput()}