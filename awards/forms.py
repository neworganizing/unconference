from django import forms
from django.contrib.auth import get_user_model
from awards.models import (MostValuableOrganizer, MostValuableTechnology,
                           MostValuableCampaign)

from awards.utils import get_user_profile_model, get_organization_model

User = get_user_model()
UserProfile = get_user_profile_model()
Organization = get_organization_model()


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    organization = forms.CharField()

    class Meta:
        exclude = ('user', 'bio')
        model = UserProfile

    def save(self, *args, **kwargs):
        user, user_created = User.objects.get_or_create(
            email=self.cleaned_data['email']
        )

        if user_created:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            setattr(user, User.USERNAME_FIELD, user.email)

        user.save()

        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None

        if not user_profile:
            user_profile = super(UserProfileForm, self).save(commit=False)
            user_profile.user = user
            org, created = Organization.objects.get_or_create(
                name=self.cleaned_data['organization']
            )
            org.save()
            user_profile.save()
            user_profile.set_organization(org)

        return user_profile


class NominatorForm(UserProfileForm):
    pass


class NomineeForm(UserProfileForm):
    pass


class AwardForm(forms.ModelForm):
    class Meta:
        exclude = (
            'profile', 'nominator', 'slug', 'approved',
            'contacted', 'personal_statement'
        )
        widgets = {'unconference': forms.HiddenInput()}


class MostValuableOrganizerSubmissionForm(AwardForm):
    award_name = 'Most Valuable Organizer'
    award_url = 'submit_mvo'
    shortname = 'MVO'
    nominee_type = 'an organizer'

    class Meta(AwardForm.Meta):
        model = MostValuableOrganizer


class MostValuableTechnologySubmissionForm(AwardForm):
    award_name = 'Most Valuable Technology'
    award_url = 'submit_mvt'
    shortname = 'MVT'
    nominee_type = 'a technology'

    class Meta(AwardForm.Meta):
        model = MostValuableTechnology
        exclude = AwardForm.Meta.exclude + ('organization', )


class MostValuableCampaignSubmissionForm(AwardForm):
    award_name = 'Most Valuable Campaign'
    award_url = 'submit_mvc'
    shortname = 'MVC'
    nominee_type = 'a campaign'

    class Meta(AwardForm.Meta):
        model = MostValuableCampaign
        exclude = AwardForm.Meta.exclude + ('organization', )


class EditForm(forms.ModelForm):
    twitter = forms.CharField(max_length=50)


class MostValuableOrganizerEditForm(EditForm):
    class Meta:
        model = MostValuableOrganizer
        fields = {'personal_statement', 'twitter'}


class MostValuableTechnologyEditForm(EditForm):
    class Meta:
        model = MostValuableTechnology
        fields = {'personal_statement', 'twitter'}


class MostValuableCampaignEditForm(EditForm):
    class Meta:
        model = MostValuableCampaign
        fields = {'personal_statement', 'twitter'}
