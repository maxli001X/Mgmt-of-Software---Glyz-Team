from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Placeholder for profile & settings dashboard.
    TODO: Implement stories #43-45 (Profile & Settings features)
    """
    return render(request, "profile_settings/dashboard.html")

