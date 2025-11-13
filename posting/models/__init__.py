# Import all models for backward compatibility
# This allows `from posting.models import Post, Tag, Vote` to work as before

from .post import Post
from .tag import Tag
from .vote import Vote

__all__ = ["Post", "Tag", "Vote"]

