from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView

from sicop.users.forms import SignUpForm
from sicop.users.models import User


class LoginView(LoginView):
    template_name = "sicop/users/login/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form),
        )

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("user_login"))


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "sicop/users/signup/signup.html"
    success_url = reverse_lazy("user_login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Tu usuario fue creado exitosamente, ahora puedes iniciar sesión."))
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form),
        )


class ArtdPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        pass
        # twilio = Twilio()
        # twilio.send_plain_email
        # body = loader.render_to_string(email_template_name, context)
        # twilio.send_html_email(to_email, "Recuperación de contraseña", body)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "sicop/users/reset/reset_password.html"
    email_template_name = "sicop/users/emails/password_reset_email.html"
    subject_template_name = "sicop/users/reset/password_reset_subject.html"
    success_url = reverse_lazy("user_password_reset_done")
    form_class = ArtdPasswordResetForm


class ResetPasswordMessageView(TemplateView):
    template_name = "sicop/users/reset/reset_password_message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user
        # context["user"] = user
        # context["coworker"] = Coworker.objects.filter(
        #     email=self.request.user.email,
        # ).first()
        # permissions = user.user_permissions.all()

        # permissions_dict = {}
        # for permission in permissions:
        #     permission_explode = permission.codename.split("_")
        #     if permission_explode[1] not in permissions_dict:
        #         permissions_dict[permission_explode[1]] = {
        #             "add": False,
        #             "change": False,
        #             "delete": False,
        #             "view": False,
        #         }
        #     if permission_explode[0] == "add":
        #         permissions_dict[permission_explode[1]]["add"] = True
        #     if permission_explode[0] == "change":
        #         permissions_dict[permission_explode[1]]["change"] = True
        #     if permission_explode[0] == "delete":
        #         permissions_dict[permission_explode[1]]["delete"] = True
        #     if permission_explode[0] == "view":
        #         permissions_dict[permission_explode[1]]["view"] = True
        # context["permissions"] = permissions_dict
        return context


class UserPasswordChangeView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/profile/password_change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if password == password_confirm:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Tu contraseña fue cambiada exitosamente."))
        else:
            messages.warning(request, _("Las contraseñas no coinciden."))
        return HttpResponseRedirect(reverse("user_password_change"))
