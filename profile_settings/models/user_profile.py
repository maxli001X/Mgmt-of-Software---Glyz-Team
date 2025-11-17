from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extended user profile with preferences."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    
    # Email notification preferences
    email_notifications_enabled = models.BooleanField(
        default=True,
        help_text="Receive email notifications for important updates"
    )
    email_on_replies = models.BooleanField(
        default=True,
        help_text="Receive emails when someone replies to your posts"
    )
    email_on_upvotes = models.BooleanField(
        default=False,
        help_text="Receive emails when your posts receive upvotes"
    )
    email_on_mentions = models.BooleanField(
        default=True,
        help_text="Receive emails when you are mentioned"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"Profile for {self.user.username}"


class Feedback(models.Model):
    """User feedback submissions."""
    FEEDBACK_TYPES = [
        ("BUG", "Bug Report"),
        ("FEATURE", "Feature Request"),
        ("QUESTION", "Question"),
        ("OTHER", "Other"),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="feedback_submissions",
        null=True,
        blank=True
    )
    feedback_type = models.CharField(
        max_length=10,
        choices=FEEDBACK_TYPES,
        default="OTHER"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
    
    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.subject}"
