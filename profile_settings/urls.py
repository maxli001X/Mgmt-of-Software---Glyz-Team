from django.urls import path

from .views import dashboard

app_name = "profile_settings"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]

