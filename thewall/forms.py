from django import forms
from thewall.models import Session, Participant

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

class CreateParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['organization']

    def __init__(self, *args, **kwargs):
        super(CreateParticipantForm, self).__init__(*args, **kwargs)
        self.fields["phone"] = forms.CharField(max_length=20, required=True)

    def save(self):
        instance = super(CreateParticipantForm, self).save()
        instance.phone = self.cleaned_data["phone"]
        instance.save()
        return instance
