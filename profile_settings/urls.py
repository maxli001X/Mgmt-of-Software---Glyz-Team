from django.urls import path

from .views import (
    change_password,
    dashboard,
    email_preferences,
    help_feedback,
    my_posts,
    privacy_policy,
    settings,
    terms_of_service,
)

app_name = "profile_settings"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("my-posts/", my_posts, name="my_posts"),
    path("settings/", settings, name="settings"),
    path("settings/change-password/", change_password, name="change_password"),
    path("settings/email-preferences/", email_preferences, name="email_preferences"),
    path("legal/terms/", terms_of_service, name="terms_of_service"),
    path("legal/privacy/", privacy_policy, name="privacy_policy"),
    path("help/", help_feedback, name="help_feedback"),
]

