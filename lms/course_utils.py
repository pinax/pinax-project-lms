"""
Contains utility functions relating to course management used in various
different places with the wider website.

TODO: Add tests!
"""
from lms.courses.models import CourseVersion, CourseInstance
from pinax.teams.models import Membership


def modules_needing_lectures(course_instance, user):
    """
    Given a course_instance and a user, will return a list of modules (and
    associated lectures) where the user needs to indicate which lecture they
    will register in.
    """
    result = []
    for module in course_instance.course_version.modules.all():
        lectures = module.lectures.filter(course_instance=course_instance)
        if lectures.count() > 1:
            has_booked = False
            for lecture in lectures:
                team = lecture.trainees_team
                if Membership.objects.filter(team=team, user=user):
                    has_booked = True
                    break
            if not has_booked:
                result.append({
                    'module': module,
                    'lectures': lectures,
                })
    return result


def courses_needing_attention(user):
    """
    Returns a list of course instances that the user is enrolled in where the
    user needs to indicate which lectures they will register for.
    """
    result = []
    for course in courses_as_trainee(user):
        if modules_needing_lectures(course, user):
            result.append(course)
    return result


def courses_as_instructor(user):
    """
    Returns a list of all the courses where the user is a member of the
    instructor's team.
    """
    courses = []
    memberships = [m for m in user.memberships.all()]
    for course in CourseVersion.objects.all():
        for membership in memberships:
            if membership.team == course.instructors_team:
                courses.append(course)
    return courses


def courses_as_trainee(user):
    """
    Returns a list of all the courses where the user is a member of the
    instructor's team.
    """
    courses = []
    for course in CourseInstance.objects.all():
        for membership in user.memberships.all():
            if membership.team == course.trainees_team:
                courses.append(course)
    return courses
