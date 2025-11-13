from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from ..models import Post, Vote


@login_required
def upvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    created = False
    if not post.votes.filter(voter=request.user).exists():
        Vote.objects.create(post=post, voter=request.user)
        created = True

    if created:
        messages.success(request, "Thanks for upvoting!")
    else:
        messages.info(request, "You already upvoted this post.")

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

