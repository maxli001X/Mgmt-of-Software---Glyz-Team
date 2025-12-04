"""Management command to clean up orphan tags (tags with no posts)."""

from django.core.management.base import BaseCommand
from django.db.models import Count

from posting.models import Tag


class Command(BaseCommand):
    """Remove tags that have no posts associated with them."""

    help = "Remove orphan tags (tags with no posts)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - no changes will be made\n"))

        # Find tags with no posts
        orphan_tags = Tag.objects.annotate(post_count=Count("posts")).filter(post_count=0)

        if not orphan_tags.exists():
            self.stdout.write(self.style.SUCCESS("No orphan tags found."))
            return

        self.stdout.write(f"Found {orphan_tags.count()} orphan tag(s):\n")

        for tag in orphan_tags:
            self.stdout.write(f"  - {tag.name} ({tag.slug})")

        if not dry_run:
            count = orphan_tags.count()
            orphan_tags.delete()
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} orphan tag(s)."))
        else:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(f"Would delete {orphan_tags.count()} orphan tag(s).")
            )
