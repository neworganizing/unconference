from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.template.defaultfilters import capfirst

from .factories import (MVOFactory, UnconferenceFactory, UserProfileFactory,
                        MVTFactory, MVCFactory, OrganizationFactory)
from .utils import get_user_profile_model

User = get_user_model()
UserProfile = get_user_profile_model()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_all_nominees(self):
        # Setup an MVO, MVT, and MVC
        unconference = UnconferenceFactory()
        mvo = MVOFactory(unconference=unconference)
        mvt = MVTFactory(unconference=unconference)
        mvc = MVCFactory(unconference=unconference)

        # Get the list_all_nominess page
        response = self.client.get(
            reverse(
                'list_award_nominees',
                kwargs={"unconference": unconference.slug}
            )
        )

        self.assertTrue(response.status_code, 200)
        self.assertIn(mvo.name, response.content)
        self.assertIn(mvt.name, response.content)
        self.assertIn(mvc.name, response.content)

    def test_list_specific_nominees(self):
        # Setup an MVO, MVT, and MVC
        unconference = UnconferenceFactory()
        mvo = MVOFactory(unconference=unconference)
        mvt = MVTFactory(unconference=unconference)
        mvc = MVCFactory(unconference=unconference)

        # Get the list_all_nominess page
        response = self.client.get(
            reverse(
                'list_award_nominees',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvo"
                }
            )
        )

        self.assertTrue(response.status_code, 200)
        self.assertIn(mvo.name, response.content)
        self.assertNotIn(mvt.name, response.content)
        self.assertNotIn(mvc.name, response.content)

    def test_show_mvo_details(self):
        # Setup unconference and nominee
        unconference = UnconferenceFactory()
        mvo = MVOFactory(unconference=unconference)

        response = self.client.get(
            reverse(
                'display_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": 'mvo',
                    "slug": mvo.slug
                }
            )
        )

        self.assertTrue(response.status_code, 200)
        self.assertIn(capfirst(mvo.name), response.content)

    def test_show_mvt_details(self):
        # Setup unconference and nominee
        unconference = UnconferenceFactory()
        mvt = MVTFactory(unconference=unconference)

        response = self.client.get(
            reverse(
                'display_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": 'mvt',
                    "slug": mvt.slug
                }
            )
        )

        self.assertTrue(response.status_code, 200)

    def test_show_mvc_details(self):
        # Setup unconference and nominee
        unconference = UnconferenceFactory()
        mvc = MVCFactory(unconference=unconference)

        response = self.client.get(
            reverse(
                'display_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": 'mvc',
                    "slug": mvc.slug
                }
            )
        )

        self.assertTrue(response.status_code, 200)

    def test_mvo_submit_form_logged_out(self):
        # Assuming an unconference, a nominee, and a nominator
        unconference = UnconferenceFactory()
        nominator = UserProfileFactory.build()
        nominee = UserProfileFactory.build()
        organization = OrganizationFactory()

        # The user navigates to the form page
        response = self.client.get(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvo"
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        # Then, the user fills out the form
        # and submits the page to create a new nomination
        data = {
            "nomination-unconference": unconference.id,
            "nomination-relationship": "colleague",
            "nomination-innovation": "Blah",
            "nomination-respect": "Blah",
            "nomination-courage": "Blah",
            "nomination-excellence": "Blah",
            "nominee-first_name": nominee.user.first_name,
            "nominee-last_name": nominee.user.last_name,
            "nominee-email": nominee.user.email,
            "nominee-organization": organization.name,
            "nominator-first_name": nominator.user.first_name,
            "nominator-last_name": nominator.user.last_name,
            "nominator-email": nominator.user.email,
            "nominator-organization": organization.name
        }

        response = self.client.post(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvo"
                }
            ),
            data
        )

        self.assertEqual(response.status_code, 302)

    def test_mvt_submit_form_logged_out(self):
        # Assuming an unconference, a nominee, and a nominator
        unconference = UnconferenceFactory()
        nominator = UserProfileFactory.build()
        nominee = UserProfileFactory.build()
        organization = OrganizationFactory()

        # The user navigates to the form page
        response = self.client.get(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvt"
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        # Then, the user fills out the form
        # and submits the page to create a new nomination
        data = {
            "nomination-name": "Great new tech!",
            "nomination-unconference": unconference.id,
            "nomination-relationship": "user",
            "nomination-innovation": "Blah",
            "nomination-potential": "Blah",
            "nomination-accessibility": "Blah",
            "nomination-additional": "Blah",
            "nominee-first_name": nominee.user.first_name,
            "nominee-last_name": nominee.user.last_name,
            "nominee-email": nominee.user.email,
            "nominee-organization": organization.name,
            "nominator-first_name": nominator.user.first_name,
            "nominator-last_name": nominator.user.last_name,
            "nominator-email": nominator.user.email,
            "nominator-organization": organization.name
        }

        response = self.client.post(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvt"
                }
            ),
            data
        )

        self.assertEqual(response.status_code, 302)

    def test_mvc_submit_form_logged_out(self):
        # Assuming an unconference, a nominee, and a nominator
        unconference = UnconferenceFactory()
        nominator = UserProfileFactory.build()
        nominee = UserProfileFactory.build()
        organization = OrganizationFactory()

        # The user navigates to the form page
        response = self.client.get(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvc"
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        # Then, the user fills out the form
        # and submits the page to create a new nomination
        data = {
            "nomination-name": "Great new campaign!",
            "nomination-unconference": unconference.id,
            "nomination-relationship": "Staff",
            "nomination-innovation": "Blah",
            "nomination-change": "Blah",
            "nomination-motivate": "Blah",
            "nomination-creative": "Blah",
            "nomination-additional": "Blah",
            "nominee-first_name": nominee.user.first_name,
            "nominee-last_name": nominee.user.last_name,
            "nominee-email": nominee.user.email,
            "nominee-organization": organization.name,
            "nominator-first_name": nominator.user.first_name,
            "nominator-last_name": nominator.user.last_name,
            "nominator-email": nominator.user.email,
            "nominator-organization": organization.name
        }

        response = self.client.post(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvc"
                }
            ),
            data
        )

        self.assertEqual(response.status_code, 302)

    def test_mvo_submit_form_logged_in(self):
        # Assuming an unconference, a nominee, and a nominator
        unconference = UnconferenceFactory()
        nominator = UserProfileFactory()
        nominee = UserProfileFactory.build()
        organization = OrganizationFactory()

        # The user is logged in
        nominator.user.set_password('test')
        nominator.user.save()

        self.client.login(
            username=getattr(nominator.user, User.USERNAME_FIELD),
            password='test'
        )

        # The user navigates to the form page
        response = self.client.get(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvo"
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        # The user fills out the form
        data = {
            "nomination-unconference": unconference.id,
            "nomination-relationship": "colleague",
            "nomination-innovation": "Blah",
            "nomination-respect": "Blah",
            "nomination-courage": "Blah",
            "nomination-excellence": "Blah",
            "nominee-first_name": nominee.user.first_name,
            "nominee-last_name": nominee.user.last_name,
            "nominee-email": nominee.user.email,
            "nominee-organization": organization.name
        }

        response = self.client.post(
            reverse(
                'submit_nominee',
                kwargs={
                    "unconference": unconference.slug,
                    "award": "mvo"
                }
            ),
            data
        )

        self.assertEqual(response.status_code, 302)
        new_nominee = UserProfile.objects.get(user__email=nominee.user.email)
        self.assertTrue(new_nominee)
        self.assertEqual(new_nominee.organization, organization)
