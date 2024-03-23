from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from sicop.budget.models import ProvisionCartAnullationReason


class AnullationReasonListViewB(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """View for AreaRole list."""

    template_name = "sicop/frontend/budget/provision/anullation/list.html"
    permission_required = "budget.view_provisioncartanullationreason"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reasons = ProvisionCartAnullationReason.objects.all()
        print("-----------------------------------------")
        print(reasons)
        print("-----------------------------------------")
        context["reasons"] = reasons
        return context


class AnullationReasonListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for AreaRole list."""

    model = ProvisionCartAnullationReason
    template_name = "sicop/frontend/budget/provision/anullation/list.html"
    context_object_name = "provision_cart_anullation_reasons"
    permission_required = "budget.view_provisioncartanullationreason"

    def queryset(self):
        return ProvisionCartAnullationReason.objects.all()


class ProvisionCartAnullationReasonDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for AreaRole detail."""

    model = ProvisionCartAnullationReason
    template_name = "sicop/frontend/budget/provision/anullation/detail.html"
    context_object_name = "provision_cart_anullation_reason"
    permission_required = "budget.view_provisioncartanullationreason"


class ProvisionCartAnullationReasonCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for AreaRole create."""

    model = ProvisionCartAnullationReason
    template_name = "sicop/frontend/budget/provision/anullation/create.html"
    fields = [
        "name",
        "description",
    ]
    context_object_name = "provision_cart_anullation_reason"
    permission_required = "budget.add_provisioncartanullationreason"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Provision Cart Anullation Reason created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Provision Cart Anullation Reason not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "anullation_reason_detail",
            kwargs={"pk": self.object.id},
        )


class ProvisionCartAnullationReasonUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for AreaRole update."""

    model = ProvisionCartAnullationReason
    template_name = "sicop/frontend/budget/provision/anullation/update.html"
    fields = [
        "name",
        "description",
        "status",
    ]
    context_object_name = "provision_cart_anullation_reason"
    permission_required = "budget.change_provisioncartanullationreason"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Provision Cart Anullation Reason updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Provision Cart Anullation Reason not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "anullation_reason_detail",
            kwargs={"pk": self.object.id},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        request.POST._mutable = True
        if request.POST.get("status") == "True":
            request.POST["status"] = True
        else:
            request.POST["status"] = False
        return super().post(request, *args, **kwargs)
