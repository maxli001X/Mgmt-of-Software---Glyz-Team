from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import YaleSignUpForm


class YaleLoginView(LoginView):
    template_name = "accounts/login.html"


class YaleLogoutView(LogoutView):
    template_name = "accounts/logout.html"


class SignUpView(CreateView):
    form_class = YaleSignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("forum:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Welcome to Tree Hole Yale!")
        return redirect(self.get_success_url())
