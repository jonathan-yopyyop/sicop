# from typing import Any

# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin  # , PermissionRequiredMixin

# from django.http import HttpRequest, HttpResponse
# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

# from sicop.budget.models import Budget, BudgetDescription
from sicop.cost_center.models import CostCenter
from sicop.project.models import Project

# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, UpdateView
# from django.views.generic.list import ListView


class BudgetProvisionCreate(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/budget/processes/provision/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(status=True)
        context["cost_centers"] = CostCenter.objects.filter(status=True)
        return context
