# Import all forms for backward compatibility
# This allows `from posting.forms import PostForm` to work as before

from .post_form import PostForm

__all__ = ["PostForm"]

