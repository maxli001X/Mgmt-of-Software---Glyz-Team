from django.db import models

class ABTestLog(models.Model):
    VARIANT_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
    ]
    EVENT_TYPE_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    variant = models.CharField(max_length=1, choices=VARIANT_CHOICES, db_index=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, db_index=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.variant} - {self.event_type}"
