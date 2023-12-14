from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.project.models import ProjectType


class ProjectTypeListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for ProjectType list."""

    model = ProjectType
    template_name = "sicop/frontend/project/type/list.html"
    context_object_name = "types"
    permission_required = "project.view_projecttype"


class ProjectTypeDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for ProjectType detail."""

    model = ProjectType
    template_name = "sicop/frontend/project/type/detail.html"
    context_object_name = "type"
    permission_required = "project.view_projecttype"


class ProjectTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for ProjectType create."""

    model = ProjectType
    template_name = "sicop/frontend/project/type/create.html"
    fields = [
        "name",
        "cap",
    ]
    permission_required = "project.add_projecttype"

    def get_success_url(self) -> str:
        """Return to ProjectType list."""
        return reverse_lazy("project_type_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project type created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.warning(self.request, _("Project type could not be created."))
        return super().form_invalid(form)


class ProjectTypeUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for ProjectType update."""

    model = ProjectType
    template_name = "sicop/frontend/project/type/update.html"
    fields = [
        "name",
        "cap",
        "status",
    ]
    context_object_name = "type"
    permission_required = "project.change_projecttype"

    def get_success_url(self) -> str:
        """Return to ProjectType list."""
        return reverse_lazy("project_type_list")

    def form_valid(self, form: HttpRequest) -> HttpResponse:
        """Validate form."""
        messages.success(self.request, _("Project type updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form: HttpRequest) -> HttpResponse:
        """Invalidate form."""
        messages.warning(self.request, _("Project type could not be updated."))
        return super().form_invalid(form)
