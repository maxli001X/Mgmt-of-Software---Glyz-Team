from django.urls import path

from . import views

app_name = "posting"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<int:pk>/upvote/", views.upvote_post, name="upvote"),
    path("posts/<int:pk>/downvote/", views.downvote_post, name="downvote"),
    path("posts/<int:pk>/flag/", views.flag_post, name="flag"),
    path("my-stats/", views.my_stats, name="my_stats"),
    path("users/", views.admin_user_list, name="admin_user_list"),
    path("stats/", views.aggregated_stats, name="aggregated_stats"),
]

