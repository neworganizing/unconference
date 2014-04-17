from django import forms
from thewall.models import Session

class NewSessionForm(forms.ModelForm):
	class Meta:
		model = Session