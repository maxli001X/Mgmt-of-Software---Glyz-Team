from django.urls import path

from .views import dashboard

app_name = "moderation_ranking"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]

