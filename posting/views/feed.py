from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, Tag


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
            return redirect("auth_landing:login")

        form = PostForm(request.POST)
        if form.is_valid():
            form.save(author=request.user)
            messages.success(request, "Post submitted successfully!")
            return redirect(reverse("posting:home"))

    tags = Tag.objects.all()

    return render(
        request,
        "posting/home.html",
        {
            "form": form,
            "posts": posts,
            "tags": tags,
            "active_tag": tag_slug,
        },
    )

