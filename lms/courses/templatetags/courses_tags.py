from django import template

from lms import course_utils

register = template.Library()


@register.assignment_tag
def courses_as_instructor(user):
    return course_utils.courses_as_instructor(user)


@register.assignment_tag
def courses_as_trainee(user):
    return course_utils.courses_as_trainee(user)


@register.assignment_tag
def courses_needing_attention(user):
    return course_utils.courses_needing_attention(user)
