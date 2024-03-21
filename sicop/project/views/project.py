from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from sicop.certificate.models import Certificate
from sicop.area.models import Area, AreaMember, AreaRole

from sicop.area.models import Area
from sicop.project.models import Project, ProjectStatus, ProjectType, ProjectStatusHistory
from sicop.users.models import User
from datetime import datetime


class ProjectListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Project list."""

    model = Project
    template_name = "sicop/frontend/project/project/list.html"
    context_object_name = "projects"
    permission_required = "project.view_project"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role
        context_data["area_member"] = area_member
        context_data["role"] = role
        return context_data

    def get_queryset(self):
        user = self.request.user
        area_member = AreaMember.objects.filter(user=user).first()
        role: AreaRole = area_member.role

        if role.code == "director":
            query_set = Project.objects.filter(
                area=area_member.area,
            )
        elif role.code == "director_administrativo":
            query_set = Project.objects.filter(
                area=area_member.area,
            )
        elif role.code == "administrator":
            query_set = Project.objects.filter(
                area=area_member.area,
            )
        else:
            query_set = Project.objects.filter(
                project_manager=user,
            )
        return query_set


class ProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Project detail."""

    model = Project
    template_name = "sicop/frontend/project/project/detail.html"
    context_object_name = "project"
    permission_required = "project.view_project"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["areas"] = Area.objects.all()
        context_data["users"] = User.objects.all()
        context_data["project_types"] = ProjectType.objects.all()
        context_data["project_statuses"] = ProjectStatus.objects.all()
        return context_data


class ProjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for Project update."""

    model = Project
    template_name = "sicop/frontend/project/project/update.html"
    fields = [
        "name",
        "description",
        "start_date",
        "end_date",
        "budget",
        "area",
        "project_type",
        "project_status",
        "project_manager",
        "is_it_taxable",
        "status",
        "is_closed",
        "closed_datetime",
    ]
    permission_required = "project.change_project"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["areas"] = Area.objects.all()
        context_data["users"] = User.objects.all()
        context_data["project_types"] = ProjectType.objects.all()
        context_data["project_statuses"] = ProjectStatus.objects.all()
        return context_data

    def get_success_url(self) -> str:
        """Return to Project list."""
        return reverse_lazy("project_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.warning(self.request, _("Project could not be updated."))
        return super().form_invalid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request.POST._mutable = True
        if request.POST.get("status") == "True":
            request.POST["status"] = True
        else:
            request.POST["status"] = False

        if request.POST.get("is_closed") == "True":
            request.POST["is_closed"] = True
            request.POST["closed_datetime"] = datetime.now()
        else:
            request.POST["is_closed"] = False

        if request.POST.get("is_it_taxable") == "True":
            request.POST["is_it_taxable"] = True
        else:
            request.POST["is_it_taxable"] = False
        current_budget = request.POST["budget"].replace(",", ".")
        request.POST["budget"] = float(current_budget)
        if request.POST["is_closed"]:
            request.POST["project_status"] = 3
            object = self.get_object()
            object_status = ProjectStatus.objects.get(id=3)
            ProjectStatusHistory.objects.create(
                project=object,
                project_status=object_status,
                comment=_("Projecto cerrado el:") + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

        return super().post(request, *args, **kwargs)


class ProjectManagerView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        area_id = kwargs["pk"]
        area = Area.objects.get(id=area_id)
        users = []
        for user in area.areamember_set.all():
            print(user.user.id)
            users.append([user.user.id, user.user.name])
        return JsonResponse(
            {
                "area_id": area_id,
                "users": users,
            }
        )


class ProjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Project
    template_name = "sicop/frontend/project/project/create.html"
    fields = [
        "name",
        "description",
        "start_date",
        "end_date",
        "budget",
        "area",
        "project_type",
        "project_status",
        "project_manager",
        "is_it_taxable",
    ]
    permission_required = "project.add_project"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["areas"] = Area.objects.all()
        context_data["users"] = User.objects.all()
        context_data["project_types"] = ProjectType.objects.all()
        context_data["project_statuses"] = ProjectStatus.objects.all()
        return context_data

    def get_success_url(self) -> str:
        """Return to Project list."""
        return reverse_lazy("project_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.warning(self.request, _("Project could not be created."))
        return super().form_invalid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request.POST._mutable = True

        if request.POST.get("is_it_taxable") == "True":
            request.POST["is_it_taxable"] = True
        else:
            request.POST["is_it_taxable"] = False
        current_budget = request.POST["budget"].replace(",", ".")
        request.POST["budget"] = float(current_budget)
        return super().post(request, *args, **kwargs)


class GetProjectByID(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        project_id = kwargs["pk"]
        project = Project.objects.get(id=project_id)
        return JsonResponse(
            {
                "project_id": project_id,
                "project_name": project.name,
                "project_description": project.description,
                "project_start_date": project.start_date,
                "project_end_date": project.end_date,
                "project_budget": project.budget,
                "project_area": project.area.name,
                "project_type": project.project_type.name,
                "project_status": project.project_status.name,
                "project_manager": project.project_manager.name,
                "project_is_it_taxable": project.is_it_taxable,
            }
        )


class ProjectCertificateteView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for Project Certificates."""

    template_name = "sicop/frontend/project/project/certificate.html"
    permission_required = "project.view_project"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        project_id = kwargs["pk"]
        project = Project.objects.get(id=project_id)
        context_data["project"] = project
        context_data["certificate_version"] = Certificate.objects.filter(slug="project").first()
        context_data["project_status_histories"] = ProjectStatusHistory.objects.filter(project=project)
        return context_data
