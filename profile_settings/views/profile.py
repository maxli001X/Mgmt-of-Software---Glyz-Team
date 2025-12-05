from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import FeedbackForm, ProfileForm
from ..models import Feedback, UserProfile
from posting.models import Post


@login_required
def dashboard(request):
    """Profile & Settings dashboard."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_settings:dashboard')
    else:
        form = ProfileForm(instance=user_profile)
    
    context = {
        'user_profile': user_profile,
        'form': form,
        'active_tab': 'dashboard'
    }
    return render(request, 'profile_settings/dashboard.html', context)


@login_required
def my_posts(request):
    """Display all posts created by the logged-in user."""
    posts = (
        Post.objects.filter(author=request.user)
        .select_related("author")
        .prefetch_related("tags", "votes")
        .order_by("-created_at")
    )
    
    return render(
        request,
        "profile_settings/my_posts.html",
        {
            "posts": posts,
        },
    )


@login_required
def settings(request):
    """Settings page with account and app preferences."""
    return render(request, "profile_settings/settings.html")


@login_required
def change_password(request):
    """Change password form."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect("profile_settings:settings")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(
        request,
        "profile_settings/change_password.html",
        {
            "form": form,
        },
    )


@login_required
def email_preferences(request):
    """Manage email notification preferences."""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Email preferences updated successfully!")
            return redirect("profile_settings:settings")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(
        request,
        "profile_settings/email_preferences.html",
        {
            "form": form,
        },
    )


def terms_of_service(request):
    """Terms of Service page."""
    return render(request, "profile_settings/terms_of_service.html")


def privacy_policy(request):
    """Privacy Policy page."""
    return render(request, "profile_settings/privacy_policy.html")


@login_required
def help_feedback(request):
    """Help & Feedback page with form."""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(
                request,
                "Thank you for your feedback! We'll review it and get back to you if needed."
            )
            return redirect("profile_settings:help_feedback")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()
    
    return render(
        request,
        "profile_settings/help_feedback.html",
        {
            "form": form,
        },
    )

