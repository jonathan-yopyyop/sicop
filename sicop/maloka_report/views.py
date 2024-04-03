from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from sicop.maloka_report.utils.area_report import (
    get_budget_by_areas,
    get_budget_by_projects_in_area,
    get_budget_by_business_unit,
    get_project_detail,
)
from sicop.area.models import Area
from sicop.project.models import Project
from sicop.business_unit.models import BusinessUnit
from sicop.cost_center.models import CostCenter
from sicop.budget.models import Budget, ProvisionCart, ProvisionCartBudget


class ReportHomeView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/home.html"
    permission_required = "maloka_report.view_report"


class ReportByAreasView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/areas.html"
    permission_required = "maloka_report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["areas"] = get_budget_by_areas()
        return context


class ReportByProjectView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/projects.html"
    permission_required = "maloka_report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_id = kwargs.get("area")
        area = Area.objects.get(id=area_id)
        context["area"] = area
        context["projects"] = get_budget_by_projects_in_area(area)
        return context


class ReportProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/area/project.html"
    permission_required = "maloka_report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get("project")
        project = Project.objects.get(id=project_id)
        area = project.area
        budgets, totals = get_project_detail(project)
        context["project"] = project
        context["budgets"] = budgets
        context["totals"] = totals
        context["area"] = area
        return context


class ReportSelectBussinesUnitView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/bussines_unit/select.html"
    permission_required = "maloka_report.view_report"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        business_unit = request.POST.get("bussines_unit")
        url = reverse_lazy(
            "report_bussines_unit",
            kwargs={"business_unit": business_unit},
        )
        return HttpResponseRedirect(url)


class ReportBussinesUnitView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/report/bussines_unit/bussines_unit.html"
    permission_required = "maloka_report.view_report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bussines_unit_id = kwargs.get("business_unit")
        busines_unit = BusinessUnit.objects.get(id=bussines_unit_id)
        cost_centers_data, graph_data = get_budget_by_business_unit(busines_unit)
        context["busines_unit"] = busines_unit
        context["cost_centers_data"] = cost_centers_data
        context["graph_data"] = graph_data
        return context
