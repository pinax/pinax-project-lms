from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from pinax.teams.models import Team
from pinax.documents.models import Folder

from lms.courses.models import (Program, Course, CourseVersion,
                                CourseInstance)
from lms.classes.models import Module
from lms.team_utils import create_teams


class TestProgram(TestCase):
    """
    Ensures the Program class works in the expected way.

    We're following the "blessed" advice from the Django team explained here:

    https://docs.djangoproject.com/en/1.8/ref/models/instances/
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")
        self.code = '101'
        self.name = 'Test Program'

    def test_create(self):
        """
        When a program is created it automatically creates the expected
        administrators_team on-the-fly.
        """
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        prog = Program.create(self.user, self.code, self.name, access)
        self.assertFalse(prog.administrators_team is None)


class TestCourse(TestCase):
    """
    Ensure the non-standard functionality we've added to the Course model
    works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")
        self.version_name = 'Test version'

    def test_create_version(self):
        """
        Ensure the CourseVersion factory works as expected.
        """
        course = Course(created_by=self.user, code='101', name='Testing')
        course.save()
        # Check the factory method.
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        cv = course.create_version(self.user, self.version_name, access)
        # Check the new course version is set up properly
        self.assertIsInstance(cv, CourseVersion)
        self.assertEqual(cv.created_by, self.user)
        self.assertEqual(cv.course, course)
        self.assertEqual(cv.version_name, self.version_name)
        self.assertFalse(cv.administrators_team is None)
        self.assertFalse(cv.instructors_team is None)
        self.assertFalse(cv.documents is None)


class TestCourseVersion(TestCase):
    """
    Ensure the non-standard functionality we've added to the CourseVersion
    model works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")
        self.course = Course(created_by=self.user, code='101', name='Testing')
        self.course.save()
        self.start_date = date.today()
        self.end_date = date(self.start_date.year + 1, self.start_date.month,
                             self.start_date.day)
        self.institution = 'The Important Institute of Testing'
        self.module_name = 'Test Module'

    def test_create_module(self):
        """
        Ensure the Module factory works as expected.
        """
        # Make a CourseVersion.
        cv_access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        cv = CourseVersion(created_by=self.user, course=self.course,
                           version_name='Test version')
        folder_name = 'Documents for {} ({})'.format(self.course.__unicode__(),
                                                     'Test version')
        docs = Folder(name=folder_name, author=self.user,
                      modified_by=self.user)
        docs.save()
        cv.documents = docs
        create_teams(cv, self.user, cv_access)
        cv.save()
        # Test the factory method.
        cm = cv.create_module(self.module_name, Module.CLASSROOM, self.user)
        # Check it's set up properly
        self.assertIsInstance(cm, Module)
        self.assertEqual(cm.created_by, self.user)
        self.assertEqual(cm.course_version, cv)
        self.assertEqual(cm.name, self.module_name)

    def test_create_instance(self):
        """
        Ensure the CourseInstance factory works as expected.
        """
        # Make a CourseVersion.
        cv_access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        cv = CourseVersion(created_by=self.user, course=self.course,
                           version_name='Test version')
        folder_name = 'Documents for {} ({})'.format(self.course.__unicode__(),
                                                     'Test version')
        docs = Folder(name=folder_name, author=self.user,
                      modified_by=self.user)
        docs.save()
        cv.documents = docs
        create_teams(cv, self.user, cv_access)
        cv.save()
        # Test the factory method.
        access = {
            'assessors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                               Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
            'teaching_assistants_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                         Team.MANAGER_ACCESS_CHOICES[0][0]),
            'trainees_team': (Team.MEMBER_ACCESS_CHOICES[0][0],
                              Team.MANAGER_ACCESS_CHOICES[0][0]),

        }
        ci = cv.create_instance(self.user, self.start_date, self.end_date,
                                self.institution, access)
        # Check it's set up properly
        self.assertIsInstance(ci, CourseInstance)
        self.assertEqual(ci.created_by, self.user)
        self.assertEqual(ci.course_version, cv)
        self.assertEqual(ci.start_date, self.start_date)
        self.assertEqual(ci.end_date, self.end_date)
        self.assertEqual(ci.institution, self.institution)
