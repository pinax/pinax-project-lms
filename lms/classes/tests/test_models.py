from datetime import date, time

from django.test import TestCase
from django.contrib.auth.models import User

from pinax.teams.models import Team

from lms.courses.models import Course
from lms.classes.models import Room, Lecture, Module


class TestModule(TestCase):
    """
    Ensures the Module class works in the expected way.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="test",
                                             email="test@test.com",
                                             password="test")
        self.course = Course(created_by=self.user, code='101', name='Testing')
        self.course.save()
        access = {
            'administrators_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                    Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        self.course_version = self.course.create_version(created_by=self.user, version_name='Test version', access=access)
        self.start_time = time(11, 0)
        self.end_time = time(12, 0)
        self.room = Room(created_by=self.user, room_name='Lecture Hall',
                         building_name='Main Building', capacity=500)
        self.room.save()
        self.max_seats = 450
        self.start_date = date.today()
        self.end_date = date(self.start_date.year + 1, self.start_date.month,
                             self.start_date.day)
        self.institution = 'The Important Institute of Testing'
        self.lecture_name = 'Test Lecture'

    def test_create_lecture(self):
        """
        Ensure the CourseInstance factory works as expected.
        """
        # Make a CourseInstance.
        ci_access = {
            'assessors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                               Team.MANAGER_ACCESS_CHOICES[0][0]),
            'instructors_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                 Team.MANAGER_ACCESS_CHOICES[0][0]),
            'teaching_assistants_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                                         Team.MANAGER_ACCESS_CHOICES[0][0]),
            'trainees_team': (Team.MEMBER_ACCESS_CHOICES[0][0],
                              Team.MANAGER_ACCESS_CHOICES[0][0]),

        }
        ci = self.course_version.create_instance(self.user, self.start_date,
                                                 self.end_date,
                                                 self.institution, ci_access)

        # Make the Module instance that we're going to test.
        m = self.course_version.create_module('test module', Module.CLASSROOM,
                                              self.user)
        # Make a new lecture
        access = {
            'trainees_team': (Team.MEMBER_ACCESS_CHOICES[2][0],
                              Team.MANAGER_ACCESS_CHOICES[0][0]),
        }
        lecture = m.create_lecture(ci, self.user,
                                   self.start_date, self.start_time,
                                   self.end_time, self.room,
                                   self.max_seats, access)
        # Check it's set up properly
        self.assertIsInstance(lecture, Lecture)
        self.assertEqual(lecture.course_instance, ci)
        self.assertEqual(lecture.module, m)
        self.assertEqual(lecture.created_by, self.user)
        self.assertEqual(lecture.course_instance, ci)
        self.assertEqual(lecture.date, self.start_date)
        self.assertEqual(lecture.start_time, self.start_time)
        self.assertEqual(lecture.end_time, self.end_time)
        self.assertEqual(lecture.room, self.room)
        self.assertEqual(lecture.max_seats, self.max_seats)
