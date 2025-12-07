from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import urlparse

from ..forms import CommentForm
from ..models import Comment, CommentVote, Post
from django.template.loader import render_to_string
from django.http import JsonResponse


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
def add_comment(request, post_pk):
    """Add a top-level comment to a post."""
    post = get_object_or_404(Post, pk=post_pk)

    if request.method != "POST":
        return redirect(reverse("posting:home"))

    form = CommentForm(request.POST, post=post)
    if form.is_valid():
        comment = form.save(author=request.user)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # return new comment html
            context = {
                'comment': comment,
                'user_comment_votes': {}, # No votes yet on new comment
                'user': request.user,
            }
            html = render_to_string('posting/components/comment_item.html', context, request=request)
            return JsonResponse({
                'success': True,
                'message': 'Comment added!',
                'html': html,
                'comment_count': post.comments.count()
            })
            
        messages.success(request, "Comment added!")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({
                'success': False,
                'message': str(form.errors.as_text())
            })
            
        for error in form.errors.get("body", []):
            messages.error(request, error)

    return _safe_redirect(request, reverse("posting:home"))


@login_required
def add_reply(request, comment_pk):
    """Add a reply to an existing comment."""
    parent_comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method != "POST":
        return redirect(reverse("posting:home"))

    # Block replies to deleted comments
    if parent_comment.is_deleted:
        messages.error(request, "Cannot reply to a deleted comment.")
        return _safe_redirect(request, reverse("posting:home"))

    form = CommentForm(
        request.POST, post=parent_comment.post, parent_comment=parent_comment
    )
    if form.is_valid():
        comment = form.save(author=request.user)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {
                'comment': comment,
                'user_comment_votes': {},
                'user': request.user,
            }
            html = render_to_string('posting/components/comment_item.html', context, request=request)
            return JsonResponse({
                'success': True,
                'message': 'Reply added!',
                'html': html
            })

        messages.success(request, "Reply added!")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({
                'success': False,
                'message': str(form.errors.as_text())
            })

        for error in form.errors.get("body", []):
            messages.error(request, error)

    return _safe_redirect(request, reverse("posting:home"))


@login_required
def upvote_comment(request, pk):
    """Handle upvote with toggle behavior."""
    if request.method != "POST":
        return redirect(reverse("posting:home"))

    comment = get_object_or_404(Comment, pk=pk)

    # Block voting on deleted comments
    if comment.is_deleted:
        messages.error(request, "Cannot vote on a deleted comment.")
        return _safe_redirect(request, reverse("posting:home"))

    existing_vote = comment.get_user_vote(request.user)

    if existing_vote is None:
        # No vote exists, create upvote (handle race condition)
        try:
            CommentVote.objects.create(
                comment=comment, voter=request.user, vote_type=CommentVote.UPVOTE
            )
            messages.success(request, "Upvote recorded.")
            user_vote = "UPVOTE"
            action = "added"
        except IntegrityError:
            # Race condition: vote was created by another request
            messages.info(request, "Vote already recorded.")
            user_vote = "UPVOTE"
            action = "none"
    elif existing_vote.vote_type == CommentVote.DOWNVOTE:
        # User has downvoted, change to upvote
        existing_vote.vote_type = CommentVote.UPVOTE
        existing_vote.save(update_fields=["vote_type"])
        messages.success(request, "Changed to upvote.")
        user_vote = "UPVOTE"
        action = "changed"
    else:
        # User has upvoted, remove vote (toggle off)
        existing_vote.delete()
        messages.info(request, "Upvote removed.")
        user_vote = None
        action = "removed"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Vote updated',
            'new_score': comment.get_net_votes(),
            'user_vote': user_vote,
            'action': action,
            'upvotes': comment.get_upvotes_count(),
            'downvotes': comment.get_downvotes_count()
        })

    return _safe_redirect(request, reverse("posting:home"))


@login_required
def downvote_comment(request, pk):
    """Handle downvote with toggle behavior."""
    if request.method != "POST":
        return redirect(reverse("posting:home"))

    comment = get_object_or_404(Comment, pk=pk)

    # Block voting on deleted comments
    if comment.is_deleted:
        messages.error(request, "Cannot vote on a deleted comment.")
        return _safe_redirect(request, reverse("posting:home"))

    existing_vote = comment.get_user_vote(request.user)

    if existing_vote is None:
        # No vote exists, create downvote (handle race condition)
        try:
            CommentVote.objects.create(
                comment=comment, voter=request.user, vote_type=CommentVote.DOWNVOTE
            )
            messages.success(request, "Downvote recorded.")
            user_vote = "DOWNVOTE"
            action = "added"
        except IntegrityError:
            # Race condition: vote was created by another request
            messages.info(request, "Vote already recorded.")
            user_vote = "DOWNVOTE"
            action = "none"
    elif existing_vote.vote_type == CommentVote.UPVOTE:
        # User has upvoted, change to downvote
        existing_vote.vote_type = CommentVote.DOWNVOTE
        existing_vote.save(update_fields=["vote_type"])
        messages.success(request, "Changed to downvote.")
        user_vote = "DOWNVOTE"
        action = "changed"
    else:
        # User has downvoted, remove vote (toggle off)
        existing_vote.delete()
        messages.info(request, "Downvote removed.")
        user_vote = None
        action = "removed"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Vote updated',
            'new_score': comment.get_net_votes(),
            'user_vote': user_vote,
            'action': action,
            'upvotes': comment.get_upvotes_count(),
            'downvotes': comment.get_downvotes_count()
        })

    return _safe_redirect(request, reverse("posting:home"))


@login_required
def flag_comment(request, pk):
    """Flag a comment for moderator review."""
    if request.method != "POST":
        return redirect(reverse("posting:home"))

    comment = get_object_or_404(Comment, pk=pk)

    # Block flagging deleted comments
    if comment.is_deleted:
        messages.error(request, "Cannot flag a deleted comment.")
        return _safe_redirect(request, reverse("posting:home"))

    if not comment.is_flagged:
        comment.is_flagged = True
        comment.save(update_fields=["is_flagged"])
        messages.success(request, "Comment flagged for review.")
        success = True
        msg = "Comment flagged for review."
    else:
        messages.info(request, "This comment is already flagged for review.")
        success = False
        msg = "This comment is already flagged for review."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': success, 'message': msg})

    return _safe_redirect(request, reverse("posting:home"))


@login_required
def delete_comment(request, pk):
    """
    Soft delete a comment (user can only delete their own).
    Preserves thread structure for replies.
    """
    if request.method != "POST":
        return redirect(reverse("posting:home"))

    comment = get_object_or_404(Comment, pk=pk)

    # Only allow author or staff to delete
    if comment.author != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete your own comments.")
        return _safe_redirect(request, reverse("posting:home"))

    if not comment.is_deleted:
        comment.is_deleted = True
        comment.save(update_fields=["is_deleted"])
        messages.success(request, "Comment deleted.")
        success = True
        msg = "Comment deleted."
    else:
        messages.info(request, "This comment is already deleted.")
        success = False
        msg = "This comment is already deleted."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': success, 'message': msg})

    return _safe_redirect(request, reverse("posting:home"))
