from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from pinax.teams.models import Team
from pinax.documents.models import Folder

from lms.team_utils import create_teams

"""
This app models classroom sessions, when and where they are and which trainees
are assigned to them.
"""


class Module(models.Model):
    """
    Represents a discrete block of learning associated with a course version.
    Such a block may be either web-based or done in person.

    If the latter is the case then a module will have at least 1 associated
    Lecture instance that is also linked to a specific course instance. This
    designates the time and place where such a module will be delivered as
    part of a course instance.
    """

    name = models.CharField(max_length=256)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    course_version = models.ForeignKey('courses.CourseVersion', related_name="modules")
    documents = models.ForeignKey(Folder,
                                  help_text="A folder containing documents associated with this module.",
                                  related_name='module_documents')

    WEB_BASED = "web-based"
    CLASSROOM = "classroom"
    ASSESSMENT = "assement"
    TYPE_CHOICES = [
        (WEB_BASED, "Web-Based Training"),
        (CLASSROOM, "Classroom"),
        (ASSESSMENT, "Assessment"),
    ]
    module_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'course_version'

    def create_lecture(self, course_instance, created_by, date, start_time,
                       end_time, room, max_seats, access):
        """
        A factory function that creates a new "lecture" instance for
        delivery of this module as part of a course instance in a certain room
        at a certain time.
        """
        lecture = Lecture(created_by=created_by,
                          course_instance=course_instance, module=self,
                          date=date, start_time=start_time, end_time=end_time,
                          room=room, max_seats=max_seats)
        create_teams(lecture, created_by, access)
        lecture.save()
        return lecture


class Room(models.Model):
    """
    A physical room in which a class takes place.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    room_name = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)  # @@@ FK?
    capacity = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "{} ({})".format(self.building_name, self.room_name)


class Lecture(models.Model):
    """
    A single session of a module for a certain course instance at a particular
    time and location.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    course_instance = models.ForeignKey('courses.CourseInstance', related_name="lectures")
    module = models.ForeignKey(Module, related_name="lectures")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Room)
    max_seats = models.IntegerField()

    # pluralname_team
    trainees_team = models.ForeignKey(Team)

    def __unicode__(self):
        return "{} ({} {} to {})".format(self.name, self.date, self.start_time, self.end_time)

    def seats_remaining(self):
        return self.max_seats - self.trainees_team.members.count()

    @property
    def name(self):
        return self.module.name
