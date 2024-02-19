from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.area.models import AreaRole


def get_code_from_name(name: str) -> str:
    code = (
        name.replace(" ", "_")
        .lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("ü", "u")
        .replace(":", "")
        .replace(";", "")
        .replace(",", "")
        .replace(".", "")
        .replace("?", "")
        .replace("¿", "")
        .replace("¡", "")
        .replace("!", "")
        .replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        .replace("{", "")
        .replace("}", "")
        .replace("=", "")
        .replace("+", "")
        .replace("-", "")
        .replace("_", "")
        .replace("*", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("|", "")
        .replace("°", "")
        .replace("¬", "")
        .replace("´", "")
        .replace("`", "")
        .replace('"', "")
        .replace("'", "")
    )
    return code


class AreaRoleListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for AreaRole list."""

    model = AreaRole
    template_name = "sicop/frontend/area/role/list.html"
    context_object_name = "area_roles"
    permission_required = "area.view_arearole"


class AreaRoleDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for AreaRole detail."""

    model = AreaRole
    template_name = "sicop/frontend/area/role/detail.html"
    context_object_name = "area_role"
    permission_required = "area.view_arearole"


class AreaRoleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for AreaRole create."""

    model = AreaRole
    template_name = "sicop/frontend/area/role/create.html"
    fields = [
        "name",
        "code",
    ]
    context_object_name = "area_role"
    permission_required = "area.add_arearole"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("AreaRole created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("AreaRole not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_role_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        request.POST._mutable = True
        name = request.POST["name"]
        request.POST["code"] = get_code_from_name(name)
        return super().post(request, *args, **kwargs)


class AreaRoleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for AreaRole update."""

    model = AreaRole
    template_name = "sicop/frontend/area/role/update.html"
    fields = [
        "name",
        "code",
        "status",
    ]
    context_object_name = "area_role"
    permission_required = "area.change_arearole"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("AreaRole updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("AreaRole not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_role_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        request.POST._mutable = True
        name = request.POST["name"]
        request.POST["code"] = get_code_from_name(name)
        if request.POST.get("status") == "True":
            request.POST["status"] = True
        else:
            request.POST["status"] = False
        return super().post(request, *args, **kwargs)
