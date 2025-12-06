# Import all views for backward compatibility
# This allows `from posting.views import home, upvote_post, downvote_post, flag_post` to work as before

from .api import suggest_tags, search_suggestions
from .comments import (
    add_comment,
    add_reply,
    delete_comment,
    downvote_comment,
    flag_comment,
    upvote_comment,
)
from .feed import home
from .post_actions import downvote_post, flag_post, upvote_post
from .user_stats import admin_user_list, aggregated_stats, my_stats

__all__ = [
    "home",
    "upvote_post",
    "downvote_post",
    "flag_post",
    "my_stats",
    "admin_user_list",
    "aggregated_stats",
    "add_comment",
    "add_reply",
    "upvote_comment",
    "downvote_comment",
    "flag_comment",
    "delete_comment",
    "suggest_tags",
    "search_suggestions",
]

