from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PostForm
from .models import Post, Tag, Vote


def home(request):
    """Homepage showing recent posts with optional tag filtering and submission form."""
    tag_slug = request.GET.get("tag")
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("tags")
        .all()
    )

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    form = PostForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must log in with your Yale account to post.")
            return redirect("accounts:login")

        form = PostForm(request.POST)
        if form.is_valid():
            form.save(author=request.user)
            messages.success(request, "Post submitted successfully!")
            return redirect(reverse("forum:home"))

    tags = Tag.objects.all()

    return render(
        request,
        "forum/home.html",
        {
            "form": form,
            "posts": posts,
            "tags": tags,
            "active_tag": tag_slug,
        },
    )


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

    return redirect(request.META.get("HTTP_REFERER", reverse("forum:home")))


@login_required
def flag_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.is_flagged:
        post.is_flagged = True
        post.save(update_fields=["is_flagged"])
        messages.success(request, "Thanks! A moderator will review this post.")
    else:
        messages.info(request, "This post is already flagged for review.")

    return redirect(request.META.get("HTTP_REFERER", reverse("forum:home")))
