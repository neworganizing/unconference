from django import forms
from thewall.models import Session, Participant

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('unconference', 'title', 'description', 'headline', 'presenters', 'tags', 'difficulty')
        widgets = {
            'title': forms.TextInput(),
            'headline': forms.TextInput(),
            'unconference': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        unconf = kwargs['initial'].get('unconference', None)

        if unconf.slug != 'testcamp':
            self.fields['presenters'].queryset = Participant.objects.filter(
                unconference=unconf
            )


class SessionScheduleForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('unconference', 'title', 'description', 'headline',
                  'presenters', 'tags', 'difficulty',
                  'slot', 'room')
        widgets = {
            'title': forms.TextInput(),
            'headline': forms.TextInput(),
            'unconference': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(SessionScheduleForm, self).__init__(*args, **kwargs)
        self.fields['presenters'].queryset = Participant.objects.filter(
            unconference=self.fields['unconference'].initial
        )

# Form to save data either to the Participant model or the User model,
# depending on whether or not the User model has a 'phone' field
class CreateParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['organization']

    def __init__(self, *args, **kwargs):
        super(CreateParticipantForm, self).__init__(*args, **kwargs)
        self.fields["phone"] = forms.CharField(max_length=20, required=True)

        # Provide initial phone if the participant exists
        if self.instance.pk:
            self.fields["phone"].initial = self.instance.phone

    def save(self):
        instance = super(CreateParticipantForm, self).save()
        instance.phone = self.cleaned_data["phone"]
        instance.save()
        return instance
