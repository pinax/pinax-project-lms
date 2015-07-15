from django.contrib import admin

from .models import Program, Course, CourseVersion, CourseInstance
from .models import ProgramCourse, OrganizationProgram, OrganizationCourseInstance


class ProgramCourseInline(admin.TabularInline):
    model = ProgramCourse
    extra = 1


class OrganizationProgramInline(admin.TabularInline):
    model = OrganizationProgram
    extra = 1


class OrganizationCourseInstanceInline(admin.TabularInline):
    model = OrganizationCourseInstance
    extra = 1


admin.site.register(
    Program,
    list_display=["code", "name"],
    inlines=[ProgramCourseInline, OrganizationProgramInline],
)

admin.site.register(
    Course,
    list_display=["code", "name"],
)

admin.site.register(
    CourseVersion,  # should this just be an inline?
    list_display=["id", "course"]
)

admin.site.register(
    CourseInstance,  # should this just be an inline?
    list_display=["id", "course"],
    inlines=[OrganizationCourseInstanceInline],
)
