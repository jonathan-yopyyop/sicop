from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView


class GroupListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Group
    template_name = "sicop/frontend/user/group/list.html"
    permission_required = "auth.view_group"
    context_object_name = "groups"


class GroupDetailView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    model = Group
    template_name = "sicop/frontend/user/group/detail.html"
    permission_required = "auth.view_group"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        activate("es")
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs["pk"])
        context["group"] = group
        context["permissions"] = Permission.objects.filter(group=group)
        return context


class GroupUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/user/group/update.html"
    permission_required = "auth.change_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs["pk"])
        group_permissions = list(
            set(
                list(
                    Permission.objects.filter(
                        group=group,
                    ).values_list("id", flat=True)
                )
            )
        )
        context["group"] = group
        context["group_permissions"] = group_permissions
        context["permissions"] = Permission.objects.filter()
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST["name"]
            permissions = request.POST.getlist("permissions[]")
            group = Group.objects.get(pk=self.kwargs["pk"])
            group.name = name
            group.permissions.clear()
            group.permissions.set(permissions)
            group.save()
            messages.success(request, _("Group updated successfully"))

        except Exception as e:
            print(e)
            messages.warning(request, _("Group not updated"))
        return HttpResponseRedirect(
            reverse(
                "user_group_update",
                kwargs={
                    "pk": self.kwargs["pk"],
                },
            )
        )


class GroupCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Group
    template_name = "sicop/frontend/user/group/create.html"
    permission_required = "auth.add_group"
    fields = [
        "name",
        "permissions",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permissions"] = Permission.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST["name"]
            permissions = request.POST.getlist("permissions[]")
            group, created = Group.objects.get_or_create(name=name)
            group.permissions.set(permissions)
            group.save()
            messages.success(request, _("Group created successfully"))
        except Exception as e:
            print(e)
            messages.success(
                request,
                _("Group not created"),
            )
        return HttpResponseRedirect(
            reverse(
                "user_group_detail",
                kwargs={"pk": group.id},
            )
        )
