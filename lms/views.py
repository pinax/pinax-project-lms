from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView

from account.mixins import LoginRequiredMixin

from .organizations.models import Organization


class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("dashboard")
        else:
            return super(HomePageView, self).get(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"


## these are here because the org app shouldn't know about courses, etc


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
