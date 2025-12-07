from django.conf import settings
from django.db import models
from django.utils import timezone

from .tag import Tag



class PostManager(models.Manager):
    def get_trending_posts(self, queryset):
        """
        Annotate and sort queryset by trending score.
        Algorithm: (recent_votes * 2 + recent_comments) / (age_hours + 2)
        """
        from django.db import connection
        from django.db.models import Count, Q, F, ExpressionWrapper, FloatField, Value
        from django.db.models.functions import Extract
        from datetime import timedelta

        now = timezone.now()
        hours_ago_24 = now - timedelta(hours=24)

        # Annotate with recent activity counts first
        queryset = queryset.annotate(
            recent_votes=Count('votes', filter=Q(votes__created_at__gte=hours_ago_24)),
            recent_comments=Count('comments', filter=Q(comments__created_at__gte=hours_ago_24, comments__is_deleted=False))
        )

        # Calculate age in hours - use database-specific approach
        if 'postgresql' in connection.vendor:
            # PostgreSQL: Extract epoch from datetime difference
            queryset = queryset.annotate(
                age_hours=ExpressionWrapper(
                    Extract(now - F('created_at'), 'epoch') / 3600.0,
                    output_field=FloatField()
                )
            )
        elif 'sqlite' in connection.vendor:
            # SQLite: Use julianday for date difference calculation
            # Calculate hours using (julianday('now') - julianday(created_at)) * 24
            queryset = queryset.extra(
                select={'age_hours': "(julianday('now') - julianday(posting_post.created_at)) * 24"}
            )
        else:
            # Fallback: calculate age using Extract with epoch
            queryset = queryset.annotate(
                age_hours=ExpressionWrapper(
                    (Extract(Value(now), 'epoch') - Extract(F('created_at'), 'epoch')) / 3600.0,
                    output_field=FloatField()
                )
            )

        # Calculate trending score
        return queryset.annotate(
            trending_score=ExpressionWrapper(
                (F('recent_votes') * 2.0 + F('recent_comments') * 1.0) / (F('age_hours') + 2.0),
                output_field=FloatField()
            )
        ).order_by('-trending_score', '-created_at')


class Post(models.Model):
    objects = PostManager()  # Add custom manager

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
        indexes = [
            models.Index(fields=["is_flagged", "-created_at"]),
            models.Index(fields=["is_flagged", "-ai_severity_score", "-created_at"]),
            models.Index(fields=["ai_flagged"]),
        ]

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

