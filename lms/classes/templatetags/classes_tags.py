from django import template

from lms.classes.models import Lecture


register = template.Library()


@register.inclusion_tag("classes/_lecture.html")
def lecture(lecture, user):
    trainee = False
    enrolled_in_course = False
    for membership in user.memberships.all():
        if membership.team == lecture.trainees_team:
            trainee = True
        if membership.team == lecture.course_instance.trainees_team:
            enrolled_in_course = True
    return {
        "lecture": lecture,
        "trainee": trainee,
        "enrolled_in_course": enrolled_in_course,
    }


@register.assignment_tag
def classes_as_trainee(user):

    classes = []
    for course in Lecture.objects.all():
        for membership in user.memberships.all():
            if membership.team == course.trainees_team:
                classes.append(course)

    return classes
