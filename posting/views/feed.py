from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, Tag


@login_required(login_url='auth_landing:landing')
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

