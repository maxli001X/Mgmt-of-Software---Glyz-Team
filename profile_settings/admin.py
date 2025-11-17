from django.contrib import admin

from .models import Feedback, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "email_notifications_enabled", "email_on_replies", "email_on_upvotes", "email_on_mentions", "updated_at"]
    list_filter = ["email_notifications_enabled", "email_on_replies", "email_on_upvotes", "email_on_mentions"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["subject", "feedback_type", "user", "is_resolved", "created_at"]
    list_filter = ["feedback_type", "is_resolved", "created_at"]
    search_fields = ["subject", "message", "user__username", "user__email"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
