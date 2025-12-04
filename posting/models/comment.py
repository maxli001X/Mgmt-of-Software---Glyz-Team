from django.conf import settings
from django.db import models
from django.utils import timezone

from .post import Post


class Comment(models.Model):
    """
    Comment model supporting nested replies.

    Top-level comments have parent_comment=None.
    Replies have parent_comment pointing to another Comment.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
        help_text="Null for top-level comments, FK to parent for replies",
    )
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    is_anonymous = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(
        default=False, help_text="Soft delete - content hidden but structure preserved"
    )

    # AI Moderation fields
    ai_flagged = models.BooleanField(
        default=False, help_text="Flagged by AI content moderation"
    )
    ai_severity_score = models.FloatField(
        null=True, blank=True, help_text="AI severity score (0-1)"
    )
    ai_categories = models.JSONField(
        null=True, blank=True, help_text="AI category scores"
    )
    show_crisis_resources = models.BooleanField(
        default=False, help_text="Show mental health resources (self-harm detected)"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "-created_at"]),
            models.Index(fields=["parent_comment", "created_at"]),
        ]

    def __str__(self) -> str:
        if self.is_deleted:
            return f"[Deleted Comment #{self.pk}]"
        preview = self.body[:50] + "..." if len(self.body) > 50 else self.body
        return f"Comment by {self.get_author_display()}: {preview}"

    def get_author_display(self):
        """Return author name or 'Anonymous'."""
        if self.is_anonymous or not self.author:
            return "Anonymous"
        return self.author.get_full_name() or self.author.username

    def get_upvotes_count(self):
        """Return the number of upvotes for this comment."""
        from .comment_vote import CommentVote
        return self.votes.filter(vote_type=CommentVote.UPVOTE).count()

    def get_downvotes_count(self):
        """Return the number of downvotes for this comment."""
        from .comment_vote import CommentVote
        return self.votes.filter(vote_type=CommentVote.DOWNVOTE).count()

    def get_net_votes(self):
        """Return the net vote count (upvotes - downvotes)."""
        return self.get_upvotes_count() - self.get_downvotes_count()

    def get_user_vote(self, user):
        """Return the user's vote for this comment, or None."""
        if not user or not user.is_authenticated:
            return None
        try:
            return self.votes.get(voter=user)
        except self.votes.model.DoesNotExist:
            return None

    def is_reply(self):
        """Check if this is a reply to another comment."""
        return self.parent_comment is not None

    def get_replies_count(self):
        """Get count of direct replies (excluding deleted)."""
        return self.replies.filter(is_deleted=False).count()
