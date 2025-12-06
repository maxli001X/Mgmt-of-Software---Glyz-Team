"""API endpoints for posting app.

This module provides AJAX/JSON API endpoints for the posting app features:
- Tag suggestions using TF-IDF similarity

These endpoints are designed for client-side JavaScript consumption and
require authentication.
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count

from ..utils.tag_suggester import get_suggester
from ..models import Tag, Post


@login_required
@require_POST
def suggest_tags(request):
    """
    AJAX endpoint for suggesting tags based on post content.

    Expects JSON body: {"title": "...", "body": "..."}
    Returns JSON: {"tags": ["tag1", "tag2", ...]}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    title = data.get("title", "")
    body = data.get("body", "")

    # Require minimum content
    if len(title) + len(body) < 20:
        return JsonResponse({"tags": []})

    suggester = get_suggester()
    suggestions = suggester.suggest(title, body, top_k=4)

    return JsonResponse({"tags": suggestions})


@login_required
def search_suggestions(request):
    """
    AJAX endpoint for search suggestions/autocomplete.
    
    Query param: q (search query)
    Returns JSON: {
        "tags": [{"name": "...", "count": ...}],
        "recent_posts": [{"id": ..., "title": "..."}]
    }
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({"tags": [], "recent_posts": []})
    
    # Get matching tags
    tags = Tag.objects.filter(name__icontains=query).annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:5]
    
    # Get recent matching posts
    posts = Post.objects.filter(
        title__icontains=query,
        is_hidden=False
    ).select_related('author').order_by('-created_at')[:3]
    
    return JsonResponse({
        "tags": [{"name": tag.name, "count": tag.post_count} for tag in tags],
        "recent_posts": [{"id": post.pk, "title": post.title} for post in posts]
    })
