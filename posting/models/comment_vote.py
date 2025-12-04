from django.conf import settings
from django.db import models

from .comment import Comment


class CommentVote(models.Model):
    """
    Vote on a comment (upvote or downvote).
    One vote per user per comment.
    """

    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"
    VOTE_TYPES = [
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    ]

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="votes"
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_votes",
    )
    vote_type = models.CharField(
        max_length=10,
        choices=VOTE_TYPES,
        default=UPVOTE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "voter")
        indexes = [
            models.Index(fields=["comment", "vote_type"]),
        ]

    def __str__(self):
        return f"{self.voter.username} {self.vote_type.lower()}d comment #{self.comment.pk}"
