from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify

from pinax.teams.models import Team

from team_utils import create_teams
from courses.models import Program
from classes.models import Room


class TestCreateTeams(TestCase):
    """
    Ensures the create_teams utility function works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")

    def test_has_team_fk(self):
        """
        The good expected case:

        The passed in object has a foreign key field to an as-yet-to-be-created
        Team instance.

        Test the Team instance is created with the expected arguments and
        linked back to the passed in object.
        """
        # A program has an administrator's team.
        p = Program(created_by=self.user, code='101', name='Testing')
        # There is no team (at the moment)
        self.assertTrue(p.administrators_team_id is None)
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        result = create_teams(p, self.user, access)
        # A team was created
        self.assertFalse(p.administrators_team is None)
        # The resulting Team has the correct default attributes.
        t = p.administrators_team
        # TODO - this is part of the workaround for team slug names
        next_pk = next(iter(instance.pk for instance in Program.objects.order_by("-pk")), 1)
        expected_name = u'{} for {} {}'.format("administrators_team", "program", next_pk)
        # expected_name = '{} for {}'.format('administrators_team',
        #                                    p.__unicode__())
        self.assertEqual(t.name, expected_name)
        self.assertEqual(t.slug, slugify(expected_name))
        self.assertEqual(t.member_access, Team.MEMBER_ACCESS_CHOICES[2][0])
        self.assertEqual(t.manager_access, Team.MANAGER_ACCESS_CHOICES[0][0])
        self.assertEqual(t.creator, self.user)
        # The return value from the function is the expected instance
        self.assertEqual(result, p)

    def test_no_team_fk(self):
        """
        A test to ensure the guard code works so an object without a FK
        relation to a Team is left untouched.
        """
        # A room does not have an associated Team.
        r = Room(created_by=self.user, room_name='Lecture Hall',
                 building_name='Medical School', capacity=500)
        # So calling the create_teams function should do nothing nor throw any
        # errors.
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        result = create_teams(r, self.user, access)
        # Just check that the return value is the same object.
        self.assertEqual(result, r)
