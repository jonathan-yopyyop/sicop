from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.area.models import Area
from sicop.cost_center.models import CostCenter


class CostCenterListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Costcenter list."""

    model = CostCenter
    template_name = "sicop/frontend/cost_center/list.html"
    context_object_name = "costcenters"
    permission_required = "cost_center.view_costcenter"


class CostCenterDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Costcenter detail."""

    model = CostCenter
    template_name = "sicop/frontend/cost_center/detail.html"
    context_object_name = "costcenter"
    permission_required = "cost_center.view_costcenter"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.all()
        return context


class CostCenterUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for Costcenter update."""

    model = CostCenter
    template_name = "sicop/frontend/cost_center/update.html"
    fields = [
        "name",
        "description",
        "status",
        "area",
    ]
    context_object_name = "costcenter"
    permission_required = "cost_center.change_costcenter"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.all()
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Cost center updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Cost center not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cost_center_detail",
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


class CostCenterCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Costcenter create."""

    model = CostCenter
    template_name = "sicop/frontend/cost_center/create.html"
    fields = [
        "name",
        "description",
        "area",
    ]
    context_object_name = "costcenter"
    permission_required = "cost_center.add_costcenter"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.all()
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Cost center created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Cost center not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "cost_center_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)
