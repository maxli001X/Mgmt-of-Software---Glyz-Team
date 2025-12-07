from django.conf import settings
from django.db import models

from .post import Post


class Vote(models.Model):
    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"
    VOTE_TYPES = [
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote_type = models.CharField(
        max_length=10,
        choices=VOTE_TYPES,
        default=UPVOTE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "voter")
        indexes = [
            models.Index(fields=["post", "vote_type"]),
        ]

    def __str__(self):
        return f"{self.voter.username} {self.vote_type.lower()}d {self.post.title}"

