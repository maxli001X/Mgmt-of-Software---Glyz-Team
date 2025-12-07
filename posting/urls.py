from django.urls import path

from . import views

app_name = "posting"

urlpatterns = [
    path("", views.home, name="home"),
    # Post actions
    path("posts/<int:pk>/upvote/", views.upvote_post, name="upvote"),
    path("posts/<int:pk>/downvote/", views.downvote_post, name="downvote"),
    path("posts/<int:pk>/flag/", views.flag_post, name="flag"),
    # Comment actions
    path("posts/<int:post_pk>/comments/add/", views.add_comment, name="add_comment"),
    path("comments/<int:comment_pk>/reply/", views.add_reply, name="add_reply"),
    path("comments/<int:pk>/upvote/", views.upvote_comment, name="upvote_comment"),
    path("comments/<int:pk>/downvote/", views.downvote_comment, name="downvote_comment"),
    path("comments/<int:pk>/flag/", views.flag_comment, name="flag_comment"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    # User stats
    path("my-stats/", views.my_stats, name="my_stats"),
    path("users/", views.admin_user_list, name="admin_user_list"),
    path("stats/", views.aggregated_stats, name="aggregated_stats"),
    # API endpoints
    path("api/suggest-tags/", views.suggest_tags, name="suggest_tags"),
    path("api/search-suggestions/", views.search_suggestions, name="search_suggestions"),
    path("api/tag-categories/", views.tag_categories, name="tag_categories"),
]

