"""Management command to clean up malformed tags.

Finds and fixes tags containing '#' symbols or spaces.
Handles compound tags like '#pet#class#class' by splitting them.
"""

import re

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.text import slugify

from posting.models import Tag


class Command(BaseCommand):
    """Clean up malformed tags containing '#' or spaces."""

    help = "Clean up malformed tags (containing # or spaces, or compound tags)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def get_or_create_clean_tag(self, name, dry_run):
        """Get or create a clean tag with proper formatting."""
        clean_name = name.strip().replace(" ", "-")
        # Remove invalid characters (keep only alphanumeric, hyphen, underscore)
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', clean_name)

        if not clean_name or len(clean_name) < 2:
            return None

        slug = slugify(clean_name)
        if not slug:
            return None

        # Check if tag exists
        existing = Tag.objects.filter(slug=slug).first()
        if existing:
            return existing

        # Create new tag
        if not dry_run:
            tag = Tag.objects.create(name=clean_name.title(), slug=slug)
            return tag
        return {"name": clean_name.title(), "slug": slug, "is_new": True}

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

        split_count = 0
        fixed_count = 0
        deleted_count = 0

        for tag in bad_tags:
            old_name = tag.name
            posts = list(tag.posts.all())

            # Check if this is a compound tag (contains multiple #)
            if '#' in tag.name:
                # Split on # and filter out empty strings
                parts = [p.strip() for p in tag.name.split('#') if p.strip()]

                if len(parts) > 1:
                    # This is a compound tag like "#pet#class#class"
                    unique_parts = list(set(parts))  # Remove duplicates
                    self.stdout.write(f"  Splitting: '{old_name}' -> {unique_parts}")

                    new_tags = []
                    for part in unique_parts:
                        new_tag = self.get_or_create_clean_tag(part, dry_run)
                        if new_tag:
                            new_tags.append(new_tag)

                    if new_tags and not dry_run:
                        # Add posts to all the new tags
                        for post in posts:
                            for new_tag in new_tags:
                                if isinstance(new_tag, Tag):
                                    post.tags.add(new_tag)
                        # Remove posts from old tag and delete it
                        tag.posts.clear()
                        tag.delete()

                    split_count += 1
                    continue
                elif len(parts) == 1:
                    # Single tag with # prefix like "#pet"
                    new_tag = self.get_or_create_clean_tag(parts[0], dry_run)
                    if new_tag:
                        if not dry_run:
                            if isinstance(new_tag, Tag) and new_tag.pk != tag.pk:
                                # Merge into existing
                                for post in posts:
                                    post.tags.add(new_tag)
                                    post.tags.remove(tag)
                                tag.delete()
                                self.stdout.write(f"  Merged: '{old_name}' -> '{new_tag.name}'")
                            else:
                                # Update in place
                                Tag.objects.filter(pk=tag.pk).update(
                                    name=parts[0].title(), slug=slugify(parts[0])
                                )
                                self.stdout.write(f"  Fixed: '{old_name}' -> '{parts[0].title()}'")
                        else:
                            self.stdout.write(f"  Fixed: '{old_name}' -> '{parts[0].title()}'")
                        fixed_count += 1
                        continue

            # Handle tags with spaces (no #)
            new_name = tag.name.replace(" ", "-").strip("-")
            while "--" in new_name:
                new_name = new_name.replace("--", "-")

            if new_name and len(new_name) >= 2:
                new_slug = slugify(new_name)
                existing = Tag.objects.filter(slug=new_slug).exclude(pk=tag.pk).first()

                if existing:
                    if not dry_run:
                        for post in posts:
                            post.tags.add(existing)
                            post.tags.remove(tag)
                        tag.delete()
                    self.stdout.write(f"  Merged: '{old_name}' -> '{existing.name}'")
                    deleted_count += 1
                else:
                    if not dry_run:
                        Tag.objects.filter(pk=tag.pk).update(
                            name=new_name.title(), slug=new_slug
                        )
                    self.stdout.write(f"  Fixed: '{old_name}' -> '{new_name.title()}'")
                    fixed_count += 1
            else:
                if not dry_run:
                    tag.posts.clear()
                    tag.delete()
                self.stdout.write(f"  Deleted: '{old_name}' (too short)")
                deleted_count += 1

        self.stdout.write("")
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Would split {split_count}, fix {fixed_count}, delete {deleted_count} tag(s)"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Split {split_count}, fixed {fixed_count}, deleted {deleted_count} tag(s)"
                )
            )
