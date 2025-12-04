"""Management command to clean up malformed tags.

Finds and fixes tags containing '#' symbols or spaces.
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.text import slugify

from posting.models import Tag


class Command(BaseCommand):
    """Clean up malformed tags containing '#' or spaces."""

    help = "Clean up malformed tags (containing # or spaces)"

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

        # Find tags with # or spaces
        bad_tags = Tag.objects.filter(Q(name__contains="#") | Q(name__contains=" "))

        if not bad_tags.exists():
            self.stdout.write(self.style.SUCCESS("No malformed tags found."))
            return

        self.stdout.write(f"Found {bad_tags.count()} malformed tag(s):\n")

        fixed_count = 0
        deleted_count = 0

        for tag in bad_tags:
            old_name = tag.name

            # Remove # and replace spaces with hyphens
            new_name = tag.name.replace("#", "").replace(" ", "-").strip("-")

            # Remove any double hyphens
            while "--" in new_name:
                new_name = new_name.replace("--", "-")

            if new_name and len(new_name) >= 2:
                # Check if a tag with this slug already exists
                new_slug = slugify(new_name)
                existing = Tag.objects.filter(slug=new_slug).exclude(pk=tag.pk).first()

                if existing:
                    # Merge: transfer posts to existing tag, delete this one
                    if not dry_run:
                        # Get all posts with this tag
                        posts = tag.posts.all()
                        for post in posts:
                            post.tags.add(existing)
                            post.tags.remove(tag)
                        tag.delete()
                    self.stdout.write(
                        f"  Merged: '{old_name}' -> '{existing.name}' (existing tag)"
                    )
                    deleted_count += 1
                else:
                    # Update the tag
                    if not dry_run:
                        tag.name = new_name.title()
                        tag.slug = new_slug
                        # Bypass validation since we're fixing
                        Tag.objects.filter(pk=tag.pk).update(
                            name=new_name.title(), slug=new_slug
                        )
                    self.stdout.write(f"  Fixed: '{old_name}' -> '{new_name.title()}'")
                    fixed_count += 1
            else:
                # Tag is too short after cleaning - delete it
                if not dry_run:
                    # Remove from all posts first
                    tag.posts.clear()
                    tag.delete()
                self.stdout.write(
                    f"  Deleted: '{old_name}' (too short after cleaning)"
                )
                deleted_count += 1

        self.stdout.write("")
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Would fix {fixed_count} tag(s), delete {deleted_count} tag(s)"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed {fixed_count} tag(s), deleted {deleted_count} tag(s)"
                )
            )
