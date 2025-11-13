from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Placeholder screen for profile & settings stories (#43–#45).
    """
    return render(request, "profile_settings/dashboard.html")
