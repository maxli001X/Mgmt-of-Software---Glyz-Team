# Import all views for backward compatibility

from .dashboard import dashboard
from .flagged_queue import flagged_queue
from .moderation_actions import (
    delete_comment_mod,
    delete_post,
    hide_comment,
    hide_post,
    unflag_comment,
    unflag_post,
    unhide_comment,
    unhide_post,
)

__all__ = [
    "dashboard",
    "flagged_queue",
    "unflag_post",
    "hide_post",
    "unhide_post",
    "delete_post",
    "unflag_comment",
    "hide_comment",
    "unhide_comment",
    "delete_comment_mod",
]

