from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import urlparse

from posting.models import Comment, Post


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
def unflag_post(request, pk):
    """Unflag a post (mark as reviewed)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    post = get_object_or_404(Post, pk=pk)

    if post.is_flagged:
        post.is_flagged = False
        post.save(update_fields=["is_flagged"])
        messages.success(request, f"Post '{post.title}' has been unflagged.")
    else:
        messages.info(request, "This post is not flagged.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def hide_post(request, pk):
    """Hide a post from public view."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    post = get_object_or_404(Post, pk=pk)

    if not post.is_hidden:
        post.is_hidden = True
        post.is_flagged = False  # Auto-unflag when hiding
        post.save(update_fields=["is_hidden", "is_flagged"])
        messages.success(
            request, f"Post '{post.title}' has been hidden from public view."
        )
    else:
        messages.info(request, "This post is already hidden.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def unhide_post(request, pk):
    """Unhide a post (restore to public view)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    post = get_object_or_404(Post, pk=pk)

    if post.is_hidden:
        post.is_hidden = False
        post.save(update_fields=["is_hidden"])
        messages.success(
            request, f"Post '{post.title}' has been restored to public view."
        )
    else:
        messages.info(request, "This post is not hidden.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def delete_post(request, pk):
    """Permanently delete a post."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    post = get_object_or_404(Post, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, f"Post '{title}' has been permanently deleted.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def unflag_comment(request, pk):
    """Unflag a comment (mark as reviewed)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    comment = get_object_or_404(Comment, pk=pk)

    if comment.is_flagged:
        comment.is_flagged = False
        comment.save(update_fields=["is_flagged"])
        messages.success(request, "Comment has been unflagged.")
    else:
        messages.info(request, "This comment is not flagged.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def hide_comment(request, pk):
    """Soft-delete a comment (hide from view)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    comment = get_object_or_404(Comment, pk=pk)

    if not comment.is_deleted:
        comment.is_deleted = True
        comment.is_flagged = False  # Auto-unflag when hiding
        comment.save(update_fields=["is_deleted", "is_flagged"])
        messages.success(request, "Comment has been hidden from view.")
    else:
        messages.info(request, "This comment is already hidden.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def unhide_comment(request, pk):
    """Restore a hidden comment (moderator action)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    comment = get_object_or_404(Comment, pk=pk)

    if comment.is_deleted:
        comment.is_deleted = False
        comment.save(update_fields=["is_deleted"])
        messages.success(request, "Comment has been restored.")
    else:
        messages.info(request, "This comment is not hidden.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))


@login_required
def delete_comment_mod(request, pk):
    """Permanently delete a comment (moderator action)."""
    if request.method != "POST":
        return redirect(reverse("moderation_ranking:flagged_queue"))

    if not request.user.is_staff:
        raise PermissionDenied

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, "Comment has been permanently deleted.")

    return _safe_redirect(request, reverse("moderation_ranking:flagged_queue"))
