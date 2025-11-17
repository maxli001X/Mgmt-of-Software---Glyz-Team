from django.urls import path

from . import views

app_name = "posting"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<int:pk>/upvote/", views.upvote_post, name="upvote"),
    path("posts/<int:pk>/downvote/", views.downvote_post, name="downvote"),
    path("posts/<int:pk>/flag/", views.flag_post, name="flag"),
]

