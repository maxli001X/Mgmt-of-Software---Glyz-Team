# Import all views for backward compatibility

from .profile import (
    change_password,
    dashboard,
    email_preferences,
    help_feedback,
    my_posts,
    privacy_policy,
    settings,
    terms_of_service,
)

__all__ = [
    "dashboard",
    "my_posts",
    "settings",
    "change_password",
    "email_preferences",
    "terms_of_service",
    "privacy_policy",
    "help_feedback",
]

