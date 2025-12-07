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
        # Only allow same-host redirects with valid schemes
        # Reject protocol-relative URLs (empty scheme with netloc)
        is_same_host = parsed.netloc == request.get_host()
        is_relative = parsed.netloc == "" and parsed.scheme == ""
        has_valid_scheme = parsed.scheme in ("", "http", "https")
        if has_valid_scheme and (is_same_host or is_relative):
            return redirect(referer)
    return redirect(default_url)


@login_required
def upvote_post(request, pk):
    """Handle upvote with toggle behavior."""
    if request.method != "POST":
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Invalid method"}, status=405)
        return redirect(reverse("posting:home"))

    return _handle_vote(request, pk, Vote.UPVOTE)


@login_required
def downvote_post(request, pk):
    """Handle downvote with toggle behavior."""
    if request.method != "POST":
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Invalid method"}, status=405)
        return redirect(reverse("posting:home"))

    return _handle_vote(request, pk, Vote.DOWNVOTE)


def _handle_vote(request, pk, vote_type):
    """Unified vote handler."""
    post = get_object_or_404(Post, pk=pk)
    existing_vote = post.get_user_vote(request.user)
    message = ""
    user_vote = None

    if existing_vote is None:
        # Create new vote
        try:
            Vote.objects.create(post=post, voter=request.user, vote_type=vote_type)
            message = "Vote recorded."
            user_vote = "UPVOTE" if vote_type == Vote.UPVOTE else "DOWNVOTE"
        except IntegrityError:
            message = "Vote already recorded."
    
    elif existing_vote.vote_type == vote_type:
        # Toggle OFF (delete existing same vote)
        existing_vote.delete()
        message = "Vote removed."
        user_vote = None
    
    else:
        # Switch vote (update existing)
        existing_vote.vote_type = vote_type
        existing_vote.save(update_fields=["vote_type"])
        message = "Vote changed."
        user_vote = "UPVOTE" if vote_type == Vote.UPVOTE else "DOWNVOTE"

    if _is_ajax(request):
        # Calculate new counts - use explicit separate queries to avoid ORM issues
        # Refresh from database to ensure we get latest counts
        upvotes = Vote.objects.filter(post_id=post.pk, vote_type=Vote.UPVOTE).count()
        downvotes = Vote.objects.filter(post_id=post.pk, vote_type=Vote.DOWNVOTE).count()

        return JsonResponse({
            "success": True,
            "message": message,
            "net_votes": upvotes - downvotes,
            "upvotes_count": upvotes,
            "downvotes_count": downvotes,
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

