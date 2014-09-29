from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10, null=True, blank=True)
    twitter_handle = models.CharField(max_length=18, null=True, blank=True)
    facebook_handle = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    zip_plus4 = models.CharField(max_length=4, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(
        upload_to='user_profiles/photos', null=True, blank=True
    )

    def __unicode__(self):
        return u"{0} {1}'s profile".format(
            self.user.first_name, self.user.last_name
        )

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def organization(self):
        try:
            organization = self.organizations.filter(
                current=True
            )[0].organization
        except IndexError:
            organization = None

        return organization

    def set_organization(self, organization):
        upo, created = UserProfileOrganization.objects.get_or_create(
            user_profile=self, organization=organization
        )

        upo.current = True
        upo.save()

    def save(self, **kwargs):
        if not self.pk:
            setattr(self.user, User.USERNAME_FIELD, self.user.email)

        return super(UserProfile, self).save(**kwargs)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(
        upload_to='organizations/logos',
        null=True,
        blank=True
    )
    group = models.ForeignKey(Group, null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, **kwargs):
        if not self.pk:
            self.abbreviation = self.generate_abbreviation()
        return super(Organization, self).save(**kwargs)

    def generate_abbreviation(self):
        words = self.name.split(" ")
        abbreviation = ""

        for word in words:
            abbreviation += word[0].upper()

        return abbreviation


class UserProfileOrganization(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, related_name="organizations"
    )
    organization = models.ForeignKey(
        Organization, related_name="members"
    )
    current = models.BooleanField(default=True)
