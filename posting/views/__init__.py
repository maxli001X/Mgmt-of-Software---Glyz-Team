# Import all views for backward compatibility
# This allows `from posting.views import home, upvote_post, flag_post` to work as before

from .feed import home
from .post_actions import flag_post, upvote_post

__all__ = ["home", "upvote_post", "flag_post"]

