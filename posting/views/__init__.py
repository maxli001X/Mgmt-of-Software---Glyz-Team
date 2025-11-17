# Import all views for backward compatibility
# This allows `from posting.views import home, upvote_post, downvote_post, flag_post` to work as before

from .feed import home
from .post_actions import downvote_post, flag_post, upvote_post
from .user_stats import admin_user_list, aggregated_stats, my_stats

__all__ = ["home", "upvote_post", "downvote_post", "flag_post", "my_stats", "admin_user_list", "aggregated_stats"]

