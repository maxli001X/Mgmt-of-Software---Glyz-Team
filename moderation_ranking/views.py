from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Placeholder screen for moderation ranking.
    TODO: Implement story #50 (Content Moderation E2E) with real data.
    """
    return render(request, "moderation_ranking/dashboard.html")
