import os

from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
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


def setup_admin(request):
    """
    TEMPORARY: One-time admin setup endpoint.
    Creates/updates admin user from environment variables.
    DELETE THIS AFTER USE.
    """
    User = get_user_model()

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@yale.edu")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if not password:
        return HttpResponse(
            "Error: DJANGO_SUPERUSER_PASSWORD not set in environment variables",
            status=400
        )

    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True}
        )

        if not created:
            user.email = email
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        return HttpResponse(
            f"Success! {action} superuser '{username}' with email '{email}'.\n"
            f"You can now login at /admin/ or /auth/login/\n\n"
            f"IMPORTANT: Remove the setup-admin URL after logging in!",
            content_type="text/plain"
        )
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)
