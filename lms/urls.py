from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

from .views import HomePageView, DashboardView
from .views import OrganizationListView, OrganizationDetailView

from lms.courses.views import CourseVersionDetailView, CourseInstanceDetailView
from lms.classes.views import ModuleDetailView


urlpatterns = patterns(
    "",
    url(r"^$", HomePageView.as_view(), name="home"),
    url(r"^dashboard/$", DashboardView.as_view(), name="dashboard"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^notifications/", include("pinax.notifications.urls")),
    url(r"^documents/", include("pinax.documents.urls")),

    url(r"^courses/(?P<pk>\d+)/$", CourseInstanceDetailView.as_view(), name="courseinstance_detail"),
    url(r"^course_version/(?P<pk>\d+)/$", CourseVersionDetailView.as_view(), name="courseversion_detail"),

    url(r"^org/$", OrganizationListView.as_view(), name="organization_list"),
    url(r"^org/(?P<slug>[\w-]+)/$", OrganizationDetailView.as_view(), name="organization_detail"),
    url(r"^invites/", include("kaleo.urls")),

    # temporary
    url(r"^courses/(?P<pk>\d+)/enroll/$", "lms.courses.views.course_enroll", name="course_enroll"),
    url(r"^courses/(?P<pk>\d+)/unenroll/$", "lms.courses.views.course_unenroll", name="course_unenroll"),

    url(r"^classes/(?P<pk>\d+)/enroll/$", "lms.classes.views.lecture_enroll", name="lecture_enroll"),
    url(r"^classes/(?P<pk>\d+)/unenroll/$", "lms.classes.views.lecture_unenroll", name="lecture_unenroll"),

    url(r"^teams/", include("pinax.teams.urls")),
    url(r"^module/(?P<pk>\d+)/$", ModuleDetailView.as_view(), name="module_detail"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
