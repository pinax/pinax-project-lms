from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify

from pinax.teams.models import Team

from lms.organizations.models import Organization


class TestOrganization(TestCase):
    """
    Ensures the Organization class works in the expected way.

    We're following the "blessed" advice from the Django team explained here:

    https://docs.djangoproject.com/en/1.8/ref/models/instances/
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")
        self.org_name = 'Important Organization'
        self.org_slug = slugify(self.org_name)

    def test_create(self):
        """
        When an organization is created it automatically creates the expected
        administrators_team on-the-fly.
        """
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        org = Organization.create(self.user, self.org_name, self.org_slug,
                                  access)
        self.assertFalse(org.administrators_team is None)
