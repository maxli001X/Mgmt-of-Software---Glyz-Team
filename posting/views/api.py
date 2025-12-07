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


@login_required
def tag_categories(request):
    """
    AJAX endpoint for getting tags grouped by category using AI.

    Returns JSON: {
        "categories": [
            {
                "name": "Courses",
                "tags": [{"name": "MGT 541", "slug": "mgt-541", "count": 5}, ...]
            },
            ...
        ]
    }
    """
    from django.db.models import Q
    from ..utils.tag_categorizer import get_categorizer

    # Get tags with at least 1 visible post
    tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_hidden=False))
    ).filter(post_count__gte=1).order_by('name')

    # Build tag info dict for quick lookup
    tag_info = {
        tag.name: {
            'name': tag.name,
            'slug': tag.slug,
            'count': tag.post_count
        }
        for tag in tags
    }

    # Get AI-powered categorization
    tag_names = list(tag_info.keys())
    categorizer = get_categorizer()
    ai_categories = categorizer.categorize_tags(tag_names)

    # Build response with full tag info
    categories = []
    for cat_name, cat_tag_names in ai_categories.items():
        cat_tags = []
        for tag_name in cat_tag_names:
            if tag_name in tag_info:
                cat_tags.append(tag_info[tag_name])
        if cat_tags:
            categories.append({
                'name': cat_name,
                'tags': cat_tags
            })

    return JsonResponse({'categories': categories})
