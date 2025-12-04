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

from ..utils.tag_suggester import get_suggester


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
