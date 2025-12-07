from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, Prefetch, Q, F, ExpressionWrapper, FloatField, Subquery, OuterRef, IntegerField
from django.db.models.functions import Extract, Coalesce
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from ..forms import PostForm
from ..models import Comment, CommentVote, Post, Tag, Vote


@login_required(login_url='auth_landing:landing')
def home(request):
    """Homepage showing recent posts with optional tag filtering, search, and submission form."""
    tag_slug = request.GET.get("tag")
    search_query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "recent")  # Default to recent
    view_mode = request.GET.get("view", "home")  # 'home' or 'posts'

    # Prefetch for nested comments (top-level only, replies handled via related_name)
    # Only prefetch non-deleted comments for display
    comments_prefetch = Prefetch(
        "comments",
        queryset=Comment.objects.filter(is_deleted=False).select_related("author").prefetch_related("votes", "replies__author", "replies__votes"),
    )

    # Base queryset with optimizations - exclude hidden posts
    # Use subqueries for vote counts to avoid JOIN multiplication issues
    # that can occur when combined with other queries (like trending)
    upvotes_subquery = Vote.objects.filter(
        post=OuterRef('pk'),
        vote_type=Vote.UPVOTE
    ).values('post').annotate(cnt=Count('id')).values('cnt')

    downvotes_subquery = Vote.objects.filter(
        post=OuterRef('pk'),
        vote_type=Vote.DOWNVOTE
    ).values('post').annotate(cnt=Count('id')).values('cnt')

    posts = (
        Post.objects.filter(is_hidden=False)
        .select_related("author", "author__profile")
        .prefetch_related("tags", "votes", comments_prefetch)
        .annotate(
            upvotes_count=Coalesce(Subquery(upvotes_subquery), 0),
            downvotes_count=Coalesce(Subquery(downvotes_subquery), 0),
            visible_comments_count=Count("comments", filter=Q(comments__is_deleted=False)),
        )
        .annotate(
            score=F('upvotes_count') - F('downvotes_count')
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
    if sort == "trending":
        try:
            posts = Post.objects.get_trending_posts(posts)
        except Exception as e:
            # Fallback to recent if trending query fails
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Trending query failed: {e}")
            posts = posts.order_by("-created_at")
    elif sort == "popular":
        # score is already annotated as upvotes - downvotes
        posts = posts.order_by("-score", "-created_at")
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

    # Get user votes for all posts and comments to check vote state in template
    user_votes = {}
    user_comment_votes = {}
    if request.user.is_authenticated:
        # Post votes
        post_votes = Vote.objects.filter(
            post__in=posts,
            voter=request.user
        ).select_related("post")
        user_votes = {vote.post_id: vote for vote in post_votes}

        # Comment votes - get all comments from these posts
        comment_votes = CommentVote.objects.filter(
            comment__post__in=posts,
            voter=request.user
        ).select_related("comment")
        user_comment_votes = {vote.comment_id: vote for vote in comment_votes}

    # Count results for screen reader announcement
    posts_count = posts.count()

    # Pagination
    paginator = Paginator(posts, 12)  # 12 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "posting/home.html",
        {
            "form": form,
            "posts": page_obj,  # Pass page_obj instead of posts
            "tags": tags,
            "active_tag": tag_slug,
            "search_query": search_query,
            "sort": sort,
            "view_mode": view_mode,
            "user_votes": user_votes,
            "user_comment_votes": user_comment_votes,
            "posts_count": posts_count,
        },
    )

