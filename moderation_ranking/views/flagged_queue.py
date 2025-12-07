from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
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
    # Annotate vote counts to avoid N+1 queries in template
    flagged_posts_qs = (
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
    flagged_comments_qs = (
        Comment.objects.filter(is_flagged=True, is_deleted=False)
        .select_related("author", "post", "parent_comment")
        .annotate(
            upvotes_count=Count("votes", filter=Q(votes__vote_type=CommentVote.UPVOTE)),
            downvotes_count=Count("votes", filter=Q(votes__vote_type=CommentVote.DOWNVOTE)),
        )
        .order_by("-ai_severity_score", "-created_at")
    )

    # Evaluate querysets once to avoid duplicate database queries
    flagged_posts_list = list(flagged_posts_qs)
    flagged_comments_list = list(flagged_comments_qs)

    # Add net_votes attribute to each item (avoids template calling model method)
    for post in flagged_posts_list:
        post.net_votes = post.upvotes_count - post.downvotes_count
    for comment in flagged_comments_list:
        comment.net_votes = comment.upvotes_count - comment.downvotes_count

    # Count AI-flagged items from already-fetched lists (no extra queries)
    ai_flagged_posts = sum(1 for p in flagged_posts_list if p.ai_flagged)
    ai_flagged_comments = sum(1 for c in flagged_comments_list if c.ai_flagged)

    # Paginate posts (25 per page)
    posts_paginator = Paginator(flagged_posts_list, 25)
    posts_page = request.GET.get("posts_page", 1)
    flagged_posts = posts_paginator.get_page(posts_page)

    # Paginate comments (25 per page)
    comments_paginator = Paginator(flagged_comments_list, 25)
    comments_page = request.GET.get("comments_page", 1)
    flagged_comments = comments_paginator.get_page(comments_page)

    context = {
        "flagged_posts": flagged_posts,
        "flagged_comments": flagged_comments,
        "flagged_posts_count": len(flagged_posts_list),
        "flagged_comments_count": len(flagged_comments_list),
        "ai_flagged_posts": ai_flagged_posts,
        "ai_flagged_comments": ai_flagged_comments,
    }

    return render(request, "moderation_ranking/flagged_queue.html", context)
