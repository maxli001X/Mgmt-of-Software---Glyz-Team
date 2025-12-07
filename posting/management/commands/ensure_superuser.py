"""
Management command to create or update a superuser from environment variables.

Unlike createsuperuser --noinput, this command:
- Creates the user if it doesn't exist
- Updates the password if the user already exists
- Never fails (safe for build scripts)
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update superuser from environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, password]):
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser creation: DJANGO_SUPERUSER_USERNAME and "
                    "DJANGO_SUPERUSER_PASSWORD environment variables required"
                )
            )
            return

        try:
            user = User.objects.get(username=username)
            # User exists - update password
            user.set_password(password)
            if email:
                user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated existing superuser: {username}")
            )
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_superuser(
                username=username,
                email=email or "",
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created new superuser: {username}")
            )
