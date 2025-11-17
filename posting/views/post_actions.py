from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from ..models import Post, Vote


@login_required
def upvote_post(request, pk):
    """Handle upvote with toggle behavior."""
    post = get_object_or_404(Post, pk=pk)
    existing_vote = post.get_user_vote(request.user)

    if existing_vote is None:
        # No vote exists, create upvote
        Vote.objects.create(post=post, voter=request.user, vote_type=Vote.UPVOTE)
        messages.success(request, "Thanks for upvoting!")
    elif existing_vote.vote_type == Vote.DOWNVOTE:
        # User has downvoted, change to upvote
        existing_vote.vote_type = Vote.UPVOTE
        existing_vote.save(update_fields=["vote_type"])
        messages.success(request, "Changed to upvote!")
    else:
        # User has upvoted, remove vote (toggle off)
        existing_vote.delete()
        messages.info(request, "Upvote removed.")

    return redirect(request.META.get("HTTP_REFERER", reverse("posting:home")))


@login_required
def downvote_post(request, pk):
    """Handle downvote with toggle behavior."""
    post = get_object_or_404(Post, pk=pk)
    existing_vote = post.get_user_vote(request.user)

    if existing_vote is None:
        # No vote exists, create downvote
        Vote.objects.create(post=post, voter=request.user, vote_type=Vote.DOWNVOTE)
        messages.success(request, "Downvote recorded.")
    elif existing_vote.vote_type == Vote.UPVOTE:
        # User has upvoted, change to downvote
        existing_vote.vote_type = Vote.DOWNVOTE
        existing_vote.save(update_fields=["vote_type"])
        messages.success(request, "Changed to downvote.")
    else:
        # User has downvoted, remove vote (toggle off)
        existing_vote.delete()
        messages.info(request, "Downvote removed.")

    return redirect(request.META.get("HTTP_REFERER", reverse("posting:home")))


@login_required
def flag_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.is_flagged:
        post.is_flagged = True
        post.save(update_fields=["is_flagged"])
        messages.success(request, "Thanks! A moderator will review this post.")
    else:
        messages.info(request, "This post is already flagged for review.")

    return redirect(request.META.get("HTTP_REFERER", reverse("posting:home")))

