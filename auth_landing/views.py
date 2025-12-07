from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import YaleSignUpForm


def landing_page(request):
    """Landing page for unauthenticated users."""
    # Redirect authenticated users to home
    if request.user.is_authenticated:
        return redirect("posting:home")
    return render(request, "auth_landing/landing.html")


class YaleLoginView(LoginView):
    template_name = "auth_landing/login.html"


class YaleLogoutView(LogoutView):
    template_name = "auth_landing/logout.html"


class SignUpView(CreateView):
    form_class = YaleSignUpForm
    template_name = "auth_landing/signup.html"
    success_url = reverse_lazy("posting:home")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, "Welcome to Tree Hole Yale!")
        return redirect(self.get_success_url())
