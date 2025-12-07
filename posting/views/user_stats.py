from datetime import datetime, timedelta, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from ..models import Post, Tag, Vote

User = get_user_model()


@login_required
def my_stats(request):
    """Display user's own statistics."""
    user = request.user
    
    # Get user's posts
    posts = Post.objects.filter(author=user)
    post_count = posts.count()
    
    # Get user's votes
    votes = Vote.objects.filter(voter=user)
    vote_count = votes.count()
    
    # Get user's flagged posts (posts they created that were flagged)
    flagged_count = posts.filter(is_flagged=True).count()
    
    # Get first post date
    first_post = posts.order_by('created_at').first()
    first_post_date = first_post.created_at if first_post else None
    
    # Get last activity date (latest post or vote)
    last_post = posts.order_by('-created_at').first()
    last_vote = votes.order_by('-created_at').first()
    
    last_activity = None
    if last_post and last_vote:
        last_activity = max(last_post.created_at, last_vote.created_at)
    elif last_post:
        last_activity = last_post.created_at
    elif last_vote:
        last_activity = last_vote.created_at
    
    # Get most used tags from user's posts
    user_tags = Tag.objects.filter(posts__author=user).annotate(
        usage_count=Count('posts', filter=Q(posts__author=user))
    ).order_by('-usage_count')[:5]
    
    # Get recent posts (last 5)
    recent_posts = posts.order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'post_count': post_count,
        'vote_count': vote_count,
        'flagged_count': flagged_count,
        'first_post_date': first_post_date,
        'last_activity': last_activity,
        'most_used_tags': user_tags,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'posting/my_stats.html', context)


@login_required
def admin_user_list(request):
    """Admin view of all users with their statistics."""
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    from django.db.models import Max

    # Use annotations to avoid N+1 queries
    users = User.objects.annotate(
        post_count=Count('posts', distinct=True),
        vote_count=Count('votes', distinct=True),
        flagged_count=Count('posts', filter=Q(posts__is_flagged=True), distinct=True),
        last_post_date=Max('posts__created_at'),
        last_vote_date=Max('votes__created_at'),
    ).order_by('-date_joined')

    # Build user_stats list with computed last_activity
    user_stats = []
    for user in users:
        last_activity = None
        if user.last_post_date and user.last_vote_date:
            last_activity = max(user.last_post_date, user.last_vote_date)
        elif user.last_post_date:
            last_activity = user.last_post_date
        elif user.last_vote_date:
            last_activity = user.last_vote_date

        user_stats.append({
            'user': user,
            'post_count': user.post_count,
            'vote_count': user.vote_count,
            'flagged_count': user.flagged_count,
            'last_activity': last_activity,
            'date_joined': user.date_joined,
        })

    # Sort by last activity (most recent first)
    # Use a very old datetime for users with no activity
    min_datetime = datetime(1970, 1, 1, tzinfo=dt_timezone.utc)
    user_stats.sort(key=lambda x: x['last_activity'] or min_datetime, reverse=True)

    context = {
        'user_stats': user_stats,
        'total_users': len(user_stats),
    }

    return render(request, 'posting/admin_user_list.html', context)


def aggregated_stats(request):
    """Public anonymized platform statistics."""
    now = timezone.now()
    
    # Total counts
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_votes = Vote.objects.count()
    total_flagged = Post.objects.filter(is_flagged=True).count()
    
    # Active users (users who have posted or voted)
    active_users = User.objects.filter(
        Q(posts__isnull=False) | Q(votes__isnull=False)
    ).distinct().count()
    
    # Daily Active Users (DAU) - users active in last 24 hours
    yesterday = now - timedelta(days=1)
    dau = User.objects.filter(
        Q(posts__created_at__gte=yesterday) | Q(votes__created_at__gte=yesterday)
    ).distinct().count()
    
    # Weekly Active Users (WAU) - users active in last 7 days
    week_ago = now - timedelta(days=7)
    wau = User.objects.filter(
        Q(posts__created_at__gte=week_ago) | Q(votes__created_at__gte=week_ago)
    ).distinct().count()
    
    # Monthly Active Users (MAU) - users active in last 30 days
    month_ago = now - timedelta(days=30)
    mau = User.objects.filter(
        Q(posts__created_at__gte=month_ago) | Q(votes__created_at__gte=month_ago)
    ).distinct().count()
    
    # Posts per day (last 7 days)
    posts_per_day = []
    for i in range(6, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_posts = Post.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()
        posts_per_day.append({
            'date': day_start.date(),
            'count': day_posts,
        })
    
    # Most popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:10]
    
    # Average posts per user
    avg_posts_per_user = total_posts / total_users if total_users > 0 else 0
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_posts': total_posts,
        'total_votes': total_votes,
        'total_flagged': total_flagged,
        'dau': dau,
        'wau': wau,
        'mau': mau,
        'posts_per_day': posts_per_day,
        'popular_tags': popular_tags,
        'avg_posts_per_user': round(avg_posts_per_user, 2),
    }
    
    return render(request, 'posting/aggregated_stats.html', context)

