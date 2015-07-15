from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from pinax.teams.models import Team, Membership
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView

from lms.classes.models import Lecture, Module


class ModuleDetailView(LoginRequiredMixin, DetailView):

    model = Module


@login_required
def lecture_enroll(request, pk):
    lecture_instance = get_object_or_404(Lecture, pk=pk)
    team = lecture_instance.trainees_team

    state = team.state_for(request.user)

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_join(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.role = Membership.ROLE_MEMBER
        membership.state = Membership.STATE_AUTO_JOINED
        membership.save()
        messages.success(request, "Enrolled in {}".format(lecture_instance))

    return redirect("courseinstance_detail", lecture_instance.course_instance.pk)


@login_required
def lecture_unenroll(request, pk):
    lecture_instance = get_object_or_404(Lecture, pk=pk)
    team = lecture_instance.trainees_team

    state = team.state_for(request.user)

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_leave(request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, "Un-enrolled from {}".format(lecture_instance))

    return redirect("courseinstance_detail", lecture_instance.course_instance.pk)
