from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from sicop.maloka_report.utils.area_report import get_budget_by_areas, get_budget_by_projects_in_area
from sicop.area.models import Area
from sicop.project.models import Project


class ReportHomeView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/home.html"
    permission_required = "report.view_report"


class ReportByAreasView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/areas.html"
    permission_required = "report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["areas"] = get_budget_by_areas()
        return context


class ReportByProjectView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/projects.html"
    permission_required = "report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_id = kwargs.get("area")
        area = Area.objects.get(id=area_id)
        context["area"] = area
        context["projects"] = get_budget_by_projects_in_area(area)
        return context


class ReportProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/project.html"
    permission_required = "report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get("project")
        project = Project.objects.get(id=project_id)
        project_budgets = project.project_budgets.all()
        area = project.area
        budgets = []
        for project_budget in project_budgets:
            budgets.append(
                {
                    "budget": project_budget,
                }
            )
        context["project"] = project
        context["budgets"] = budgets
        context["area"] = area
        return context
