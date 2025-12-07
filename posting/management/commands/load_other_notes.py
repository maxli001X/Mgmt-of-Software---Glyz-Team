"""One-time command to load 8 other notes to production."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posting.models import Post, Tag

User = get_user_model()


class Command(BaseCommand):
    """Load 8 non-class-review posts to production."""

    help = "Load other notes (non-class-review posts) to production"

    def handle(self, *args, **options):
        # Get or create admin user for author (posts are anonymous anyway)
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        if not admin_user:
            self.stdout.write(self.style.ERROR("No user found to assign as author"))
            return

        posts_data = [
            {
                "title": "Hello new version",
                "body": "new gerion #excited",
                "is_anonymous": False,
                "tags": ["excited"],
            },
            {
                "title": "Test Post - Typing Works!",
                "body": "This is a test post to verify that typing works correctly in the content area. Testing the fixes we made!",
                "is_anonymous": True,
                "tags": [],
            },
            {
                "title": "hi",
                "body": "HI #HI",
                "is_anonymous": True,
                "tags": ["hi"],
            },
            {
                "title": "hey",
                "body": "hey",
                "is_anonymous": True,
                "tags": ["hey"],
            },
            {
                "title": "sd",
                "body": "sd",
                "is_anonymous": False,
                "tags": ["sd"],
            },
            {
                "title": "Fix verify",
                "body": "#fixed",
                "is_anonymous": True,
                "tags": ["fixed"],
            },
            {
                "title": "hi",
                "body": "hi",
                "is_anonymous": False,
                "tags": ["hi"],
            },
            {
                "title": "hello",
                "body": "hi",
                "is_anonymous": False,
                "tags": ["hi"],
            },
        ]

        created_count = 0
        for data in posts_data:
            # Check if post already exists (by title and body)
            if Post.objects.filter(title=data["title"], body=data["body"]).exists():
                self.stdout.write(f"  Skipped (exists): {data['title']}")
                continue

            # Create post
            post = Post.objects.create(
                title=data["title"],
                body=data["body"],
                author=admin_user,
                is_anonymous=data["is_anonymous"],
            )

            # Add tags
            for tag_slug in data["tags"]:
                tag, _ = Tag.objects.get_or_create(
                    slug=tag_slug,
                    defaults={"name": tag_slug.title()}
                )
                post.tags.add(tag)

            self.stdout.write(f"  Created: {data['title']}")
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"\nCreated {created_count} posts")
        )
