from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a variable key."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def smart_date(value):
    """
    Format date:
    - If < 24 hours: 'X time ago' (using timesince)
    - If > 24 hours: 'MMM D, HH:MM' (e.g. Dec 6, 23:45)
    """
    from django.utils import timezone
    from django.utils.timesince import timesince
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.days < 1:
        return f"{timesince(value)} ago"
    else:
        # Format: Dec 06, 23:45 (No seconds)
        return value.strftime("%b %d, %H:%M")
