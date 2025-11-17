from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, Tag


@login_required(login_url='auth_landing:landing')
def home(request):
    """Homepage showing recent posts with optional tag filtering, search, and submission form."""
    from django.db.models import Count, Q
    
    tag_slug = request.GET.get("tag")
    search_query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "recent")  # Default to recent
    
    # Base queryset with optimizations
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("tags", "votes")
        .annotate(
            upvotes_count=Count("votes", filter=Q(votes__vote_type="UPVOTE")),
            downvotes_count=Count("votes", filter=Q(votes__vote_type="DOWNVOTE")),
        )
    )

    # Apply search filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )

    # Apply tag filter
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    # Apply sorting
    if sort == "popular":
        from django.db.models import F
        posts = posts.annotate(
            net_votes=F("upvotes_count") - F("downvotes_count")
        ).order_by("-net_votes", "-created_at")
    else:
        posts = posts.order_by("-created_at")

    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(author=request.user)
            messages.success(request, "Post submitted successfully!")
            return redirect(reverse("posting:home"))

    # Get all tags with post counts
    tags = Tag.objects.annotate(post_count=Count("posts")).order_by("name")

    # Get user votes for all posts to check vote state in template
    user_votes = {}
    if request.user.is_authenticated:
        from ..models import Vote
        votes = Vote.objects.filter(
            post__in=posts,
            voter=request.user
        ).select_related("post")
        user_votes = {vote.post_id: vote for vote in votes}

    # Count results for screen reader announcement
    posts_count = posts.count()

    return render(
        request,
        "posting/home.html",
        {
            "form": form,
            "posts": posts,
            "tags": tags,
            "active_tag": tag_slug,
            "search_query": search_query,
            "sort": sort,
            "user_votes": user_votes,
            "posts_count": posts_count,
        },
    )

