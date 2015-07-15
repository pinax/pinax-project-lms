from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from lms.organizations.models import Organization
from lms.classes.models import Module
from lms.team_utils import create_teams
from pinax.teams.models import Team
from pinax.documents.models import Folder


class Program(models.Model):
    """
    An ordered list of courses.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    administrators_team = models.ForeignKey(Team,
                                            help_text="To contain users who administer the program.")

    def __unicode__(self):
        if self.code:
            return "{}: {}".format(self.code, self.name)
        else:
            return self.name

    @classmethod
    def create(cls, created_by, code, name, access):
        """
        See: https://docs.djangoproject.com/en/1.8/ref/models/instances/ for
        the reason why I'm doing this.

        The use case is simply that upon instantiation of a Program the
        expected administrators_team is also generated on-the-fly.
        """
        prog = cls(created_by=created_by, code=code, name=name)
        return create_teams(prog, created_by, access)


class Course(models.Model):
    """
    An abstract course that may have different versions and be run multiple
    times.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        if self.code:
            return "{}: {}".format(self.code, self.name)
        else:
            return self.name

    def create_version(self, created_by, version_name, access):
        """
        A factory method that creates a new version of this course.
        """
        cv = CourseVersion(created_by=created_by, course=self,
                           version_name=version_name)
        create_teams(cv, created_by, access)
        folder_name = 'Documents for {} ({})'.format(self.__unicode__(),
                                                     version_name)
        docs = Folder(name=folder_name, author=created_by,
                      modified_by=created_by)
        docs.save()
        cv.documents = docs
        cv.save()
        return cv


class CourseVersion(models.Model):
    """
    A particular version of a Course.

    Content may vary from version to version. A single version may be run
    multiple times as separate CourseInstanes.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    course = models.ForeignKey(Course)

    administrators_team = models.ForeignKey(Team,
                                            help_text="For those who administer the course.",
                                            related_name='courseversion_admins')
    instructors_team = models.ForeignKey(Team,
                                         help_text="For those who create the course content.",
                                         related_name='courseversion_instructors')  # For academics who teach

    # Ensure a unique version name using user derived convention.
    version_name = models.CharField(max_length=100,
                                    help_text="A unique descriptive name for this version of the course.")

    documents = models.ForeignKey(Folder,
                                  help_text="A folder containing documents associated with this version of the course.",
                                  related_name='courseversion_documents')

    def __unicode__(self):
        return u'{} ({})'.format(self.course.name, self.version_name)  # @@@ incorporate version number when we have it

    class Meta:
        unique_together = [("created_at", "version_name")]
        permissions = (
            ('upload_documents', 'Can upload documents to the course version'),
            ('download_documents', 'Can download documents from a course version'),
            ('update_documents', 'Can update documents associated with a course version'),
            ('delete_documents', 'Can delete documents associated with a course version'),
        )

    def create_instance(self, created_by, start_date, end_date, institution,
                        access):
        """
        A factory method to create an instance of this version of a course.

        For example, this version may represent Medicine 101 (revision 2) and
        the course instance created by this method represents this course
        delivered in a certain time / place.

        The created_by argument is needed to facilitate the associated
        automatic team generation and it (and the other args) also populate
        the resulting CourseInstance.
        """
        ci = CourseInstance(created_by=created_by, course_version=self,
                            start_date=start_date, end_date=end_date,
                            institution=institution)
        create_teams(ci, created_by, access)
        ci.save()
        return ci

    def create_module(self, name, module_type, created_by):
        """
        A factory function that creates a new "lecture" instance for
        delivery of the course instance in a certain room at a certain time.
        """
        module = Module(name=name, created_by=created_by,
                        module_type=module_type, course_version=self)
        folder_name = 'Documents for module: {}'.format(name)
        docs = Folder(name=folder_name, author=created_by,
                      modified_by=created_by)
        docs.save()
        module.documents = docs
        module.save()
        return module


class CourseInstance(models.Model):
    """
    A particular run of a particular version of a particular course.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    course_version = models.ForeignKey(CourseVersion)

    instructors_team = models.ForeignKey(Team,
                                         help_text="For those who deliver the course.",
                                         related_name="courseinstance_instructors")  # These people deliver
    trainees_team = models.ForeignKey(Team,
                                      help_text="For those taking the course.",
                                      related_name="courseinstance_trainees")
    teaching_assistants_team = models.ForeignKey(Team,
                                                 help_text="For those assisting in the delivery of the course.",
                                                 related_name="courseinstance_teaching_assistants")
    assessors_team = models.ForeignKey(Team,
                                       help_text="For those assessing the trainees taking the course.",
                                       related_name="courseinstance_assessors")

    start_date = models.DateField()
    end_date = models.DateField()
    institution = models.CharField(max_length=100)

    @property
    def course(self):
        return self.course_version.course

    def __unicode__(self):
        """
        This is used to create slugs for things like teams. Ergo its a bit
        of a hack.
        """
        return u'{} {}-{} ({})'.format(self.course.name, self.start_date,
                                       self.end_date, self.institution)


# @@@ it's entirely possible this should be course instance, not course but
# punting for now as part of a larger question around programs
class ProgramCourse(models.Model):
    """
    The placement of a course in a program.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    program = models.ForeignKey(Program)
    sequence = models.IntegerField(null=True)
    course_version = models.ForeignKey(CourseVersion)

    @property
    def course(self):
        return self.course_version.course


class OrganizationProgram(models.Model):
    """
    The placement of a program under an organization.

    It is modelled as a many-to-many like this so a program can be under more
    than one organization.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    organization = models.ForeignKey(Organization)
    program = models.ForeignKey(Program)

    class Meta:
        unique_together = [("organization", "program")]


class OrganizationCourseInstance(models.Model):
    """
    The placement of a course instance under an organization.

    It is modelled as a many-to-many like this so a course instance can be under
    more than one organization.
    """

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    organization = models.ForeignKey(Organization)
    course_instance = models.ForeignKey(CourseInstance)

    class Meta:
        unique_together = [("organization", "course_instance")]
