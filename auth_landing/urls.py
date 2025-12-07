from django.urls import path

from .views import SignUpView, YaleLoginView, YaleLogoutView, landing_page, setup_admin

app_name = "auth_landing"

urlpatterns = [
    path("", landing_page, name="landing"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", YaleLoginView.as_view(), name="login"),
    path("logout/", YaleLogoutView.as_view(), name="logout"),
    # TEMPORARY: Remove after admin is set up
    path("setup-admin-x7k9m/", setup_admin, name="setup_admin"),
]

