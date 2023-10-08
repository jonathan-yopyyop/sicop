from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from sicop.users.models import User


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = "sicop/frontend/user/user/list.html"
    permission_required = "auth.view_user"
    context_object_name = "users"


class UsetDetailView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/user/user/detail.html"
    permission_required = "auth.view_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs["pk"])
        context["user"] = user
        user_group = None
        if user.groups.all().count() > 0:
            user_group = user.groups.all()[0]
        context["user_group"] = user_group
        context["groups"] = Group.objects.all()
        return context


class UserCreateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/user/user/create.html"
    permission_required = "auth.add_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            is_staff = request.POST.get("is_staff")
            group_id = request.POST.get("group")
            if is_staff == "on":
                is_staff = True
            else:
                is_staff = False
            if User.objects.filter(email=email).count() == 0:
                group = Group.objects.get(id=group_id)
                admin_user = User.objects.create_user(
                    name=name,
                    email=email,
                    password=password,
                    is_staff=is_staff,
                )
                group.user_set.add(admin_user)
                messages.success(request, _(f"User {email} created successfully"))
            else:
                messages.warning(request, f"User {email} already exists")
        except Exception as e:
            messages.warning(request, f"Error creating user {email}: {e}")
        return HttpResponseRedirect(reverse("user_list"))


class UserUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/user/user/update.html"
    permission_required = "auth.change_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs["pk"])
        user_group = None
        if user.groups.all().count() > 0:
            user_group = user.groups.all()[0]
        context["user_group"] = user_group
        context["user"] = user
        context["groups"] = Group.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            is_staff = request.POST.get("is_staff")
            is_active = request.POST.get("is_active")
            group_id = request.POST.get("group")
            password = request.POST.get("password")
            if is_staff == "on":
                is_staff_bool = True
            else:
                is_staff_bool = False

            if is_active == "on":
                is_active_bool = True
            else:
                is_active_bool = False

            user = User.objects.get(pk=self.kwargs["pk"])
            user.name = name
            user.email = email
            user.is_staff = is_staff_bool
            user.is_active = is_active_bool
            user.groups.clear()
            group = Group.objects.get(id=group_id)
            group.user_set.add(user)
            if password is not None and password != "":
                user.set_password(password)
            user.save()
            messages.success(request, _(f"User {email} updated successfully"))
        except Exception as e:
            messages.warning(request, f"Error updating user {email}: {e}")
        return HttpResponseRedirect(reverse("user_list"))


class UserProfileUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/user/user/profile.html"
    permission_required = "auth.change_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        user_group = None
        if user.groups.all().count() > 0:
            user_group = user.groups.all()[0]
        context["user_group"] = user_group
        context["user"] = user
        context["groups"] = Group.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            password = request.POST.get("password")
            password_confirm = request.POST.get("password_confirm")
            user = User.objects.get(pk=self.request.user.pk)
            if password != password_confirm:
                messages.warning(request, f"Error updating user {user.email}: Passwords do not match")
                return HttpResponseRedirect(reverse("user_profile_update"))

            if password:
                user.name = user.name
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)

            messages.success(request, _(f"User {user.email} updated successfully"))
        except Exception as e:
            messages.warning(request, f"Error updating user {user.email}: {e}")
        return HttpResponseRedirect(reverse("user_profile_update"))
