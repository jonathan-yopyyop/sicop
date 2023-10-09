from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "sicop/frontend/home.html"
    login_url = reverse_lazy("user_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
