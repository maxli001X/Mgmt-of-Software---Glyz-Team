from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import urlparse

from ..models import Post, Vote


def _is_ajax(request):
    """Check if request is AJAX."""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def _safe_redirect(request, default_url):
    """
    Safely redirect to HTTP_REFERER, validating it's from the same host.
    Falls back to default_url if REFERER is missing or from a different host.
    """
    referer = request.META.get("HTTP_REFERER")
    if referer:
        parsed = urlparse(referer)
        if parsed.netloc == "" or parsed.netloc == request.get_host():
            return redirect(referer)
    return redirect(default_url)


@login_required
def upvote_post(request, pk):
    """Handle upvote with toggle behavior."""
    if request.method != "POST":
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Invalid method"}, status=405)
        return redirect(reverse("posting:home"))

    post = get_object_or_404(Post, pk=pk)
    existing_vote = post.get_user_vote(request.user)
    message = ""
    user_vote = None

    if existing_vote is None:
        # No vote exists, create upvote (handle race condition)
        try:
            Vote.objects.create(post=post, voter=request.user, vote_type=Vote.UPVOTE)
            message = "Upvote recorded."
            user_vote = "UPVOTE"
        except IntegrityError:
            # Race condition: vote was created by another request
            message = "Vote already recorded."
    elif existing_vote.vote_type == Vote.DOWNVOTE:
        # User has downvoted, change to upvote
        existing_vote.vote_type = Vote.UPVOTE
        existing_vote.save(update_fields=["vote_type"])
        message = "Changed to upvote."
        user_vote = "UPVOTE"
    else:
        # User has upvoted, remove vote (toggle off)
        existing_vote.delete()
        message = "Upvote removed."
        user_vote = None

    if _is_ajax(request):
        # Refresh post to get updated vote counts
        post.refresh_from_db()
        return JsonResponse({
            "success": True,
            "message": message,
            "net_votes": post.get_net_votes(),
            "upvotes_count": post.get_upvotes_count(),
            "downvotes_count": post.get_downvotes_count(),
            "user_vote": user_vote
        })

    messages.success(request, message)
    return _safe_redirect(request, reverse("posting:home"))


@login_required
def downvote_post(request, pk):
    """Handle downvote with toggle behavior."""
    if request.method != "POST":
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Invalid method"}, status=405)
        return redirect(reverse("posting:home"))

    post = get_object_or_404(Post, pk=pk)
    existing_vote = post.get_user_vote(request.user)
    message = ""
    user_vote = None

    if existing_vote is None:
        # No vote exists, create downvote (handle race condition)
        try:
            Vote.objects.create(post=post, voter=request.user, vote_type=Vote.DOWNVOTE)
            message = "Downvote recorded."
            user_vote = "DOWNVOTE"
        except IntegrityError:
            # Race condition: vote was created by another request
            message = "Vote already recorded."
    elif existing_vote.vote_type == Vote.UPVOTE:
        # User has upvoted, change to downvote
        existing_vote.vote_type = Vote.DOWNVOTE
        existing_vote.save(update_fields=["vote_type"])
        message = "Changed to downvote."
        user_vote = "DOWNVOTE"
    else:
        # User has downvoted, remove vote (toggle off)
        existing_vote.delete()
        message = "Downvote removed."
        user_vote = None

    if _is_ajax(request):
        # Refresh post to get updated vote counts
        post.refresh_from_db()
        return JsonResponse({
            "success": True,
            "message": message,
            "net_votes": post.get_net_votes(),
            "upvotes_count": post.get_upvotes_count(),
            "downvotes_count": post.get_downvotes_count(),
            "user_vote": user_vote
        })

    messages.success(request, message)
    return _safe_redirect(request, reverse("posting:home"))


@login_required
def flag_post(request, pk):
    """Flag a post for moderator review."""
    if request.method != "POST":
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Invalid method"}, status=405)
        return redirect(reverse("posting:home"))

    post = get_object_or_404(Post, pk=pk)
    if not post.is_flagged:
        post.is_flagged = True
        post.save(update_fields=["is_flagged"])
        message = "Post flagged for review."
        success = True
    else:
        message = "This post is already flagged for review."
        success = False

    if _is_ajax(request):
        return JsonResponse({"success": success, "message": message})

    if success:
        messages.success(request, message)
    else:
        messages.info(request, message)
    return _safe_redirect(request, reverse("posting:home"))

