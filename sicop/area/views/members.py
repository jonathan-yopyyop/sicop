from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from sicop.area.models import Area, AreaMember, AreaRole
from sicop.users.models import User


class AreaMemberListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """View for AreaMember list."""

    model = AreaMember
    template_name = "sicop/frontend/area/member/list.html"
    context_object_name = "members"
    permission_required = "area.view_areamember"


class AreaMemberDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """View for AreaMember detail."""

    model = AreaMember
    template_name = "sicop/frontend/area/member/detail.html"
    context_object_name = "member"
    permission_required = "area.view_areamember"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.filter(status=True)
        context["users"] = User.objects.filter(is_active=True)
        context["roles"] = AreaRole.objects.filter(status=True)
        return context


class AreaMemberUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """View for AreaMember update."""

    model = AreaMember
    template_name = "sicop/frontend/area/member/update.html"
    context_object_name = "member"
    permission_required = "area.change_areamember"
    fields = [
        "user",
        "area",
        "status",
        "role",
        "job_title",
    ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.filter(status=True)
        context["users"] = User.objects.filter(is_active=True)
        context["roles"] = AreaRole.objects.filter(status=True)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Area member updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Area member not updated, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_member_detail",
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


class AreaMemberCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """View for AreaMember create."""

    model = AreaMember
    template_name = "sicop/frontend/area/member/create.html"
    permission_required = "area.add_areamember"
    fields = [
        "user",
        "area",
        "role",
        "job_title",
    ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Create a query that return a list of users in areas
        users_in_areas = list(AreaMember.objects.filter().values_list("id", flat=True))
        context["areas"] = Area.objects.filter(status=True)
        context["users"] = User.objects.filter(is_active=True).exclude(id__in=users_in_areas)
        context["roles"] = AreaRole.objects.filter(status=True)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, _("Area member created successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, _("Area member not created, please review the data"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "area_member_detail",
            kwargs={"pk": self.object.id},
        )
