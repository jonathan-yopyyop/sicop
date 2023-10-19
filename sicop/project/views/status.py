from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.project.models import ProjectStatus


class ProjectStatusListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for ProjectStatus list."""

    model = ProjectStatus
    template_name = "sicop/frontend/project/status/list.html"
    context_object_name = "statuses"
    permission_required = "project.view_projectstatus"


class ProjectStatusDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for ProjectStatus detail."""

    model = ProjectStatus
    template_name = "sicop/frontend/project/status/detail.html"
    context_object_name = "status"
    permission_required = "project.view_projectstatus"


class ProjectStatusCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for ProjectStatus create."""

    model = ProjectStatus
    template_name = "sicop/frontend/project/status/create.html"
    fields = [
        "name",
    ]
    permission_required = "project.add_projectstatus"

    def get_success_url(self) -> str:
        """Return to ProjectStatus list."""
        return reverse_lazy("project_status_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project status created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.error(self.request, _("Project status could not be created."))
        return super().form_invalid(form)


class ProjectStatusUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for ProjectStatus update."""

    model = ProjectStatus
    template_name = "sicop/frontend/project/status/update.html"
    context_object_name = "status"
    fields = [
        "name",
        "status",
    ]
    permission_required = "project.change_projectstatus"

    def get_success_url(self) -> str:
        """Return to ProjectStatus list."""
        return reverse_lazy("project_status_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project status updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.error(self.request, _("Project status could not be updated."))
        return super().form_invalid(form)
