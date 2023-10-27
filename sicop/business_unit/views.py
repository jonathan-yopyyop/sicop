from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.business_unit.models import BusinessUnit
from sicop.cost_center.models import CostCenter


class BusinessUnitListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for Businessunit list."""

    model = BusinessUnit
    template_name = "sicop/frontend/business_unit/list.html"
    context_object_name = "businessunits"
    permission_required = "business_unit.view_businessunit"


class BusinessUnitDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for Businessunit detail."""

    model = BusinessUnit
    template_name = "sicop/frontend/business_unit/detail.html"
    context_object_name = "businessunit"
    permission_required = "business_unit.view_businessunit"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        business_units = BusinessUnit.objects.get(pk=self.kwargs["pk"])
        context["cost_centers"] = business_units.cost_centers.all()
        return context


class BusinessUnitUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for Businessunit update."""

    model = BusinessUnit
    template_name = "sicop/frontend/business_unit/update.html"
    fields = [
        "name",
        "status",
        "cost_centers",
    ]
    context_object_name = "businessunit"
    permission_required = "business_unit.change_businessunit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        business_unit = BusinessUnit.objects.get(pk=self.kwargs["pk"])
        # --
        business_units = BusinessUnit.objects.all().exclude(id=self.kwargs["pk"])
        cost_centers_to_exclude = []
        for business_unit_temp in business_units:
            cost_c = business_unit_temp.cost_centers.all()
            for cost in cost_c:
                cost_centers_to_exclude.append(cost.id)
        # --
        print(cost_centers_to_exclude)
        cost_centers = list(business_unit.cost_centers.all().values_list("id", flat=True))
        print(f"======> {pk} {business_unit.id} {cost_centers}")
        context["business_unit"] = business_unit
        context["cost_centers"] = cost_centers
        context["cost_center_all"] = CostCenter.objects.all().exclude(id__in=cost_centers_to_exclude)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Business unit updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, show the invalid form."""
        messages.error(self.request, _("Business unit not updated, please review the data"))
        return super().form_invalid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs):
        try:
            name = request.POST["name"]
            expense_type_status = request.POST["status"]
            status = False
            if expense_type_status == "True":
                status = True
            cost_centers = request.POST.getlist("cost_centers[]")
            business_unit = BusinessUnit.objects.get(pk=self.kwargs["pk"])
            business_unit.name = name
            business_unit.status = status
            business_unit.cost_centers.clear()
            business_unit.cost_centers.set(cost_centers)
            business_unit.save()
            messages.success(request, _("Business unit updated successfully."))
            return HttpResponseRedirect(
                reverse(
                    "business_unit_detail",
                    kwargs={"pk": self.kwargs["pk"]},
                )
            )

        except Exception as e:
            print(e)
            messages.error(request, _("Business unit not updated."))
            return HttpResponseRedirect(
                reverse(
                    "business_unit_detail",
                    kwargs={"pk": self.kwargs["pk"]},
                )
            )


class BusinessUnitCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for Businessunit create."""

    model = BusinessUnit
    template_name = "sicop/frontend/business_unit/create.html"
    fields = [
        "name",
        "cost_centers",
    ]
    context_object_name = "businessunit"
    permission_required = "business_unit.add_businessunit"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        business_units = BusinessUnit.objects.all()
        cost_centers = []
        for business_unit in business_units:
            cost_c = business_unit.cost_centers.all()
            for cost in cost_c:
                cost_centers.append(cost.id)
        context["cost_centers_all"] = CostCenter.objects.all().exclude(id__in=cost_centers)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Business unit created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """If the form is invalid, show the invalid form."""
        messages.error(self.request, _("Business unit not created, please review the data"))
        return super().form_invalid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        try:
            name = request.POST["name"]
            cost_centers = request.POST.getlist("cost_centers[]")
            business_unit = BusinessUnit.objects.create(name=name)
            business_unit.cost_centers.set(cost_centers)
            business_unit.save()
            messages.success(request, _("Business unit created successfully."))
            return HttpResponseRedirect(
                reverse(
                    "business_unit_detail",
                    kwargs={"pk": business_unit.id},
                )
            )
        except Exception as e:
            print(e)
            messages.error(request, _("Business unit not created."))
            return HttpResponseRedirect(
                reverse(
                    "business_unit_create",
                )
            )
