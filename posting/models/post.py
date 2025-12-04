from django.conf import settings
from django.db import models
from django.utils import timezone

from .tag import Tag


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    is_anonymous = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    is_hidden = models.BooleanField(
        default=False, help_text="Hidden by moderator - excluded from public view"
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
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_upvotes_count(self):
        """Return the number of upvotes for this post."""
        return self.votes.filter(vote_type="UPVOTE").count()

    def get_downvotes_count(self):
        """Return the number of downvotes for this post."""
        return self.votes.filter(vote_type="DOWNVOTE").count()

    def get_net_votes(self):
        """Return the net vote count (upvotes - downvotes)."""
        return self.get_upvotes_count() - self.get_downvotes_count()

    def get_vote_score(self):
        """Return vote score for sorting (same as net votes)."""
        return self.get_net_votes()

    def get_user_vote(self, user):
        """Return the user's vote for this post, or None if they haven't voted."""
        if not user or not user.is_authenticated:
            return None
        try:
            return self.votes.get(voter=user)
        except self.votes.model.DoesNotExist:
            return None

