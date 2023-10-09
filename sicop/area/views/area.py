from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.area.models import Area


class AreaListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Area list."""

    model = Area
    template_name = "sicop/frontend/area/area/list.html"
    context_object_name = "areas"
    permission_required = "area.view_area"


class AreaDetailView(LoginRequiredMixin, DetailView):
    """View for Area detail."""

    model = Area
    template_name = "sicop/frontend/area/area/detail.html"
    context_object_name = "area"
    permission_required = "area.view_area"


class AreaUpdateView(LoginRequiredMixin, UpdateView):
    """View for Area update."""

    model = Area
    template_name = "sicop/frontend/area/area/update.html"
    fields = [
        "name",
        "description",
        "status",
    ]
    context_object_name = "area"
    permission_required = "area.change_area"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Area updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Area not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_area_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        if request.POST.get("status") == "True":
            request.POST._mutable = True
            request.POST["status"] = True
        else:
            request.POST._mutable = True
            request.POST["status"] = False
        print(request.POST)
        return super().post(request, *args, **kwargs)


class AreaCreateView(LoginRequiredMixin, CreateView):
    """View for Area create."""

    model = Area
    template_name = "sicop/frontend/area/area/create.html"
    fields = [
        "name",
        "description",
        "status",
    ]
    context_object_name = "area"
    permission_required = "area.add_area"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Area created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Area not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_area_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        if request.POST.get("status") == "True":
            request.POST._mutable = True
            request.POST["status"] = True
        else:
            request.POST._mutable = True
            request.POST["status"] = False
        print(request.POST)
        return super().post(request, *args, **kwargs)
