from django.views.generic import DetailView

from account.mixins import LoginRequiredMixin

from pinax.teams.forms import TeamInviteUserForm

from .models import CourseVersion, CourseInstance

from lms import course_utils


class CourseInstanceDetailView(LoginRequiredMixin, DetailView):

    model = CourseInstance

    # TODO: prevent access if Team.MEMBER_ACCESS_INVITATION and state is None

    def trainees_team_info(self):
        course_instance = self.get_object()
        team = course_instance.trainees_team

        return {
            "team": team,
            "state": team.state_for(self.request.user),
            "role": team.role_for(self.request.user),
            "invite_form": TeamInviteUserForm(team=team),
            "can_join": team.can_join(self.request.user),
            "can_leave": team.can_leave(self.request.user),
            "can_apply": team.can_apply(self.request.user),
        }

    def modules_needing_lectures(self):
        """
        Return an ordered list of dicts containing a module and associated
        list of lectures IF the user is not enrolled in one of the lectures.
        """
        course_instance = self.get_object()
        user = self.request.user
        return course_utils.modules_needing_lectures(course_instance, user)

    def is_enrolled(self):
        """
        Returns a boolean flag to indicate if the current user is enrolled in
        the course instance.
        """
        course_instance = self.get_object()
        team = course_instance.trainees_team
        return team.can_leave(self.request.user)


## the following is copied from pinax-teams so I can customize it until such
## time as pinax-teams supports the necessary flexibility

from account.decorators import login_required
from pinax.teams.models import Team, Membership
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


@login_required
def course_enroll(request, pk):
    course_instance = get_object_or_404(CourseInstance, pk=pk)
    team = course_instance.trainees_team

    state = team.state_for(request.user)

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_join(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.role = Membership.ROLE_MEMBER
        membership.state = Membership.STATE_AUTO_JOINED
        membership.save()
        # Ensure all those modules with a single lecture associated with
        # this course instance have the user automatically enrolled in said
        # lecture.
        for module in course_instance.course_version.modules.all():
            lectures = module.lectures.filter(course_instance=course_instance)
            if lectures.count() == 1:
                team = lectures[0].trainees_team
                membership, created = Membership.objects.get_or_create(team=team, user=request.user)
                membership.role = Membership.ROLE_MEMBER
                membership.state = Membership.STATE_AUTO_JOINED
                membership.save()

        messages.success(request, "Enrolled in {}".format(course_instance))

    return redirect("courseinstance_detail", course_instance.pk)


@login_required
def course_unenroll(request, pk):
    course_instance = get_object_or_404(CourseInstance, pk=pk)
    team = course_instance.trainees_team

    state = team.state_for(request.user)

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_leave(request.user) and request.method == "POST":
        # Remove the user from the course
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        # Ensure they're removed from the lectures too.
        for lecture in course_instance.lectures.all():
            lecture_team = lecture.trainees_team
            try:
                membership = Membership.objects.get(team=lecture_team,
                                                    user=request.user)
                membership.delete()
            except Membership.DoesNotExist:
                pass  # They didn't enroll for that lecture.
        messages.success(request, "Un-enrolled from {}".format(course_instance))

    return redirect("courseinstance_detail", course_instance.pk)


class CourseVersionDetailView(LoginRequiredMixin, DetailView):

    model = CourseVersion
