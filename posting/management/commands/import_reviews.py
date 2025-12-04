"""Management command to import class reviews from Excel file.

Imports reviews as anonymous posts with #pastclassreview tag and sentiment tags.
"""

import re

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from posting.models import Post, Tag

User = get_user_model()


class Command(BaseCommand):
    """Import class reviews from Excel file as anonymous posts."""

    help = "Import class reviews from Excel file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            nargs="?",
            default="Past Review Shared in Bidding_Slack Channel.xlsx",
            help="Path to the Excel file",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def clean_text(self, text):
        """Clean mojibake and encoding issues from text."""
        if not text or pd.isna(text):
            return ""

        text = str(text)

        # Common mojibake patterns to clean
        replacements = {
            "‚Äö√Ñ√∂‚àö√ë‚àö¬•": "'",
            "‚Äö√Ñ√∂‚àö√ë¬¨‚àÇ": "",
            "‚Äö√Ñ√∂‚àö√ë‚àö√ª": "'",
            "‚Äö√Ñ√∂": "",
            "‚àö√ë": "",
            "‚àö¬•": "'",
            "‚Äô": "'",
            "‚Äù": '"',
            "‚Äú": '"',
            "‚Ä¶": "...",
            "‚Äî": "-",
            "‚Äì": "-",
            "√±": "n",
            "√©": "e",
            "√°": "a",
            "\u2019": "'",
            "\u2018": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2026": "...",
            "\u2014": "-",
            "\u2013": "-",
        }

        for bad, good in replacements.items():
            text = text.replace(bad, good)

        # Remove any remaining non-printable characters except newlines
        text = "".join(
            char for char in text if char.isprintable() or char in "\n\r\t"
        )

        # Clean up extra whitespace
        text = re.sub(r" +", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def get_or_create_tag(self, tag_name):
        """Get or create a tag by name."""
        tag_name = tag_name.strip().lower().replace("#", "")

        if not tag_name or len(tag_name) < 2:
            return None

        tag_slug = slugify(tag_name)
        if not tag_slug:
            return None

        tag, created = Tag.objects.get_or_create(
            slug=tag_slug,
            defaults={"name": tag_name.title().replace("-", " ").title().replace(" ", "-")}
        )

        if created:
            # Fix the name format
            display_name = tag_name.replace("-", " ").title().replace(" ", "-")
            if tag.name != display_name:
                Tag.objects.filter(pk=tag.pk).update(name=display_name)
                tag.refresh_from_db()

        return tag

    def get_sentiment_tag(self, sentiment_label):
        """Map sentiment label to tag name."""
        if not sentiment_label or pd.isna(sentiment_label):
            return None

        sentiment = str(sentiment_label).lower().strip()

        if "highly recommend" in sentiment:
            return "recommended"
        elif "not recommend" in sentiment:
            return "not-recommended"
        elif sentiment == "recommend":
            return "recommended"
        elif "neutral" in sentiment or "mixed" in sentiment:
            return "mixed-review"

        return None

    def handle(self, *args, **options):
        file_path = options["file_path"]
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - no changes will be made\n"))

        # Read Excel file
        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        self.stdout.write(f"Found {len(df)} rows in Excel file\n")

        # Get or create system user for authoring posts
        author = User.objects.filter(is_staff=True).first()
        if not author:
            author = User.objects.first()

        if not author:
            self.stdout.write(self.style.ERROR("No users found. Please create a user first."))
            return

        self.stdout.write(f"Using author: {author.username}\n")

        # Get or create the main tag
        pastclassreview_tag = self.get_or_create_tag("pastclassreview")
        if not pastclassreview_tag and not dry_run:
            self.stdout.write(self.style.ERROR("Could not create pastclassreview tag"))
            return

        created_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            course_code = self.clean_text(row.get("course_code", ""))
            course_name = self.clean_text(row.get("course name", ""))
            review_text = self.clean_text(row.get("review_text", ""))
            sentiment_label = row.get("sentiment_label", "")

            # Skip rows without review text
            if not review_text:
                skipped_count += 1
                continue

            # Build title
            if course_code and course_name:
                title = f"{course_code} - {course_name}"
            elif course_name:
                title = course_name
            elif course_code:
                title = course_code
            else:
                title = "Class Review"

            # Truncate title if too long
            if len(title) > 200:
                title = title[:197] + "..."

            # Build body with sentiment badge
            body = review_text
            sentiment_tag_name = self.get_sentiment_tag(sentiment_label)

            if dry_run:
                self.stdout.write(f"  Would create: {title[:60]}...")
                self.stdout.write(f"    Tags: pastclassreview" + (f", {sentiment_tag_name}" if sentiment_tag_name else ""))
                created_count += 1
            else:
                # Create the post
                post = Post.objects.create(
                    title=title,
                    body=body,
                    author=author,
                    is_anonymous=True,
                )

                # Add tags
                post.tags.add(pastclassreview_tag)

                if sentiment_tag_name:
                    sentiment_tag = self.get_or_create_tag(sentiment_tag_name)
                    if sentiment_tag:
                        post.tags.add(sentiment_tag)

                created_count += 1

        self.stdout.write("")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Would create {created_count} post(s), skip {skipped_count} row(s)"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {created_count} post(s), skipped {skipped_count} row(s)"
                )
            )
