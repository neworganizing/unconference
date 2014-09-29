import factory
import datetime

from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from thewall.models import Unconference, Venue, Day
from .models import (MostValuableOrganizer, MostValuableTechnology,
                     MostValuableCampaign)
from .utils import get_user_profile_model, get_organization_model

User = get_user_model()
UserProfile = get_user_profile_model()
Organization = get_organization_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', )

    first_name = factory.Sequence(lambda n: "jane{0}".format(n))
    last_name = 'Doe'
    email = factory.LazyAttribute(
        lambda u: "{0}.{1}@example.com".format(
            u.first_name, u.last_name
        ).lower()
    )
    username = factory.LazyAttribute(
        lambda u: "{0}".format(u.email)
    )


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: "org_{0}".format(n))


class DayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Day

    day = datetime.datetime.today()
    name = factory.LazyAttribute(
        lambda d: "{0}".format(d.day.weekday())
    )


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue

    name = factory.Sequence(lambda n: "place_{0}".format(n))
    address1 = "123 Main Street"
    city = "Anytown"
    region = "NY"
    postal = "10001"


class UnconferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unconference
        django_get_or_create = ('name', )

    name = factory.Sequence(lambda n: "unconf_{0}".format(n))
    slug = factory.LazyAttribute(
        lambda u: "{0}".format(slugify(u.name))
    )

    venue = factory.SubFactory(VenueFactory)

    @factory.post_generation
    def days(self, create, extracted, **kwargs):
        if not create:
            # simple build, do nothing
            return

        self.days.add(DayFactory())


class MVOFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MostValuableOrganizer

    profile = factory.SubFactory(UserProfileFactory)
    nominator = factory.SubFactory(UserProfileFactory)
    approved = True


class MVTFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MostValuableTechnology

    profile = factory.SubFactory(UserProfileFactory)
    nominator = factory.SubFactory(UserProfileFactory)
    organization = factory.SubFactory(OrganizationFactory)
    approved = True
    name = factory.Sequence(lambda n: "tech_{0}".format(n))


class MVCFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MostValuableCampaign

    profile = factory.SubFactory(UserProfileFactory)
    nominator = factory.SubFactory(UserProfileFactory)
    organization = factory.SubFactory(OrganizationFactory)
    approved = True
    name = factory.Sequence(lambda n: "campaign_{0}".format(n))
