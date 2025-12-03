from django.contrib import admin
from .models import ABTestLog

@admin.register(ABTestLog)
class ABTestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'variant', 'event_type', 'session_key')
    list_filter = ('variant', 'event_type', 'timestamp')
    search_fields = ('session_key', 'ip_address')
    readonly_fields = ('timestamp', 'variant', 'event_type', 'session_key', 'ip_address', 'user_agent')
