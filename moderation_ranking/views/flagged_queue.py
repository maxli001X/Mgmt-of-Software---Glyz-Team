from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render

from posting.models import Comment, CommentVote, Post, Vote


@login_required
def flagged_queue(request):
    """
    Moderator dashboard showing all flagged posts and comments.
    Staff only.
    """
    if not request.user.is_staff:
        raise PermissionDenied

    # Get all flagged posts (not hidden)
    # Sort by AI severity (high severity first), then by created date
    flagged_posts = (
        Post.objects.filter(is_flagged=True)
        .select_related("author")
        .prefetch_related("tags")
        .annotate(
            upvotes_count=Count("votes", filter=Q(votes__vote_type=Vote.UPVOTE)),
            downvotes_count=Count("votes", filter=Q(votes__vote_type=Vote.DOWNVOTE)),
        )
        .order_by("-ai_severity_score", "-created_at")
    )

    # Get all flagged comments (not deleted)
    # Sort by AI severity (high severity first), then by created date
    flagged_comments = (
        Comment.objects.filter(is_flagged=True, is_deleted=False)
        .select_related("author", "post", "parent_comment")
        .annotate(
            upvotes_count=Count("votes", filter=Q(votes__vote_type=CommentVote.UPVOTE)),
            downvotes_count=Count("votes", filter=Q(votes__vote_type=CommentVote.DOWNVOTE)),
        )
        .order_by("-ai_severity_score", "-created_at")
    )

    # Count AI-flagged items
    ai_flagged_posts = flagged_posts.filter(ai_flagged=True).count()
    ai_flagged_comments = flagged_comments.filter(ai_flagged=True).count()

    context = {
        "flagged_posts": flagged_posts,
        "flagged_comments": flagged_comments,
        "flagged_posts_count": flagged_posts.count(),
        "flagged_comments_count": flagged_comments.count(),
        "ai_flagged_posts": ai_flagged_posts,
        "ai_flagged_comments": ai_flagged_comments,
    }

    return render(request, "moderation_ranking/flagged_queue.html", context)
