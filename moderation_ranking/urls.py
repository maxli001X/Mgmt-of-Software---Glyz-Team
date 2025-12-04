from django.urls import path

from .views import (
    dashboard,
    delete_comment_mod,
    delete_post,
    flagged_queue,
    hide_comment,
    hide_post,
    unflag_comment,
    unflag_post,
    unhide_comment,
    unhide_post,
)

app_name = "moderation_ranking"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("flagged/", flagged_queue, name="flagged_queue"),
    # Post moderation actions
    path("posts/<int:pk>/unflag/", unflag_post, name="unflag_post"),
    path("posts/<int:pk>/hide/", hide_post, name="hide_post"),
    path("posts/<int:pk>/unhide/", unhide_post, name="unhide_post"),
    path("posts/<int:pk>/delete/", delete_post, name="delete_post"),
    # Comment moderation actions
    path("comments/<int:pk>/unflag/", unflag_comment, name="unflag_comment"),
    path("comments/<int:pk>/hide/", hide_comment, name="hide_comment"),
    path("comments/<int:pk>/unhide/", unhide_comment, name="unhide_comment"),
    path("comments/<int:pk>/delete/", delete_comment_mod, name="delete_comment"),
]

