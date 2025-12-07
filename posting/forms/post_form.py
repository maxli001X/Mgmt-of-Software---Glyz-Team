import re

from django import forms
from django.utils.text import slugify

from ..models import Post, Tag


class PostForm(forms.ModelForm):
    """Form for creating posts with tag support via input field and hashtags."""
    
    tags_input = forms.CharField(
        required=False,
        label="Tags",
        help_text="Enter tags separated by commas, or use #hashtag in your post body",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "e.g., academics, campus-life, events",
            "id": "id_tags_input"
        })
    )
    
    class Meta:
        model = Post
        fields = ("title", "body", "is_anonymous")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "body": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-textarea",
                "placeholder": "Share your thoughts... Use #hashtag to add tags!"
            }),
        }
        labels = {
            "title": "Title",
            "body": "Post Content",
            "is_anonymous": "Post anonymously",
        }

    post_as_identity = forms.BooleanField(
        required=False,
        label="Post with my Profile Identity",
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing post, populate tags_input with current tags
        if self.instance and self.instance.pk:
            tag_names = [tag.name for tag in self.instance.tags.all()]
            self.fields["tags_input"].initial = ", ".join(tag_names)
    
    def clean_tags_input(self):
        """Clean and normalize tag input.

        Validates that tags:
        - Are between 2-50 characters
        - Do not contain '#' symbols (except leading one which is stripped)
        - Do not contain spaces
        """
        tags_input = self.cleaned_data.get("tags_input", "").strip()

        if tags_input:
            # Validate individual tags
            for tag in tags_input.split(","):
                # Remove leading # and whitespace
                tag = tag.strip().lstrip("#").strip()
                if tag:
                    # Check for embedded # symbols
                    if '#' in tag:
                        raise forms.ValidationError(f"Tag '{tag}' cannot contain '#' symbol.")
                    # Check for spaces
                    if ' ' in tag:
                        raise forms.ValidationError(f"Tag '{tag}' cannot contain spaces. Use hyphens instead.")
                    if len(tag) < 2:
                        raise forms.ValidationError(f"Tag '{tag}' is too short (min 2 characters).")
                    if len(tag) > 50:
                        raise forms.ValidationError(f"Tag '{tag}' is too long (max 50 characters).")

        return tags_input
    
    def extract_hashtags(self, text):
        """Extract hashtags from text body."""
        if not text:
            return []
        
        # Find all hashtags: # followed by alphanumeric characters and hyphens
        # Pattern: #word or #word-word (allows letters, numbers, hyphens, underscores)
        hashtag_pattern = r'#([a-zA-Z0-9_-]+)'
        matches = re.findall(hashtag_pattern, text)
        
        # Normalize: lowercase and remove duplicates
        hashtags = []
        for match in matches:
            tag = match.lower().strip()
            # Only include valid length tags
            if tag and 2 <= len(tag) <= 50:
                hashtags.append(tag)
                
        return list(set(hashtags))  # Remove duplicates
    
    def get_or_create_tag(self, tag_name):
        """Get or create a tag by name.

        Sanitizes the tag name by:
        - Removing any '#' symbols
        - Rejecting tags with spaces
        - Enforcing length limits (2-50 chars)

        Returns None if tag is invalid.
        """
        tag_name = tag_name.strip().lower()
        if not tag_name:
            return None

        # Remove any # symbols
        tag_name = tag_name.replace('#', '')

        # Reject if contains spaces
        if ' ' in tag_name:
            return None

        # Validate length after cleaning
        if not (2 <= len(tag_name) <= 50):
            return None

        # Create slug from tag name
        tag_slug = slugify(tag_name)
        if not tag_slug:
            return None

        # Get or create tag
        tag, created = Tag.objects.get_or_create(
            slug=tag_slug,
            defaults={"name": tag_name.title()}  # Capitalize first letter of each word
        )
        return tag
    
    def save(self, commit=True, author=None):
        """Save post and handle tags from both input field and hashtags."""
        post = super().save(commit=False)
        if author is not None:
            post.author = author

        # Run quick crisis check (synchronous, instant)
        self._run_ai_moderation(post)

        # Handle identity choice
        # If post_as_identity is True, is_anonymous is False
        # If post_as_identity is False, is_anonymous is True
        post.is_anonymous = not self.cleaned_data.get('post_as_identity', False)

        if commit:
            post.save()

            # Collect all tags from both sources
            all_tags = []

            # 1. Get tags from tags_input field
            tags_input_str = self.cleaned_data.get("tags_input", "").strip()
            if tags_input_str:
                # Split by comma and clean each tag
                tag_list = []
                for tag in tags_input_str.split(","):
                    tag = tag.strip()
                    if tag:
                        # Remove any # symbols from manual input (we'll handle hashtags separately)
                        tag = tag.lstrip("#").strip()
                        if tag:
                            tag_list.append(tag)

                for tag_name in tag_list:
                    tag = self.get_or_create_tag(tag_name)
                    if tag:
                        all_tags.append(tag)

            # 2. Extract hashtags from body text
            body_text = self.cleaned_data.get("body", "")
            hashtags = self.extract_hashtags(body_text)

            for tag_name in hashtags:
                tag = self.get_or_create_tag(tag_name)
                if tag:
                    all_tags.append(tag)

            # Remove duplicates (in case same tag appears in both sources)
            unique_tags = list(set(all_tags))

            # Set tags on post
            post.tags.set(unique_tags)

            # Run full AI moderation async (background thread)
            # This updates ai_flagged, ai_severity_score, etc. after post is saved
            try:
                from django.conf import settings
                if getattr(settings, 'OPENAI_API_KEY', None):
                    from ..utils.ai_moderator import run_moderation_async
                    text = f"{post.title}\n\n{post.body}"
                    run_moderation_async(post.pk, text)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to start async moderation: {e}")

        return post

    def _run_ai_moderation(self, post, run_async=True):
        """
        Run AI content moderation on the post.

        Uses a two-phase approach for fast posting:
        1. Quick keyword check (synchronous) - detects obvious crisis content immediately
        2. Full AI moderation (async) - runs in background after post saves

        Sets show_crisis_resources immediately if crisis keywords detected.
        Full ai_flagged, ai_severity_score, ai_categories updated async.
        """
        import logging
        logger = logging.getLogger(__name__)

        text = f"{post.title}\n\n{post.body}"

        # Phase 1: Quick crisis keyword check (instant, no API call)
        from ..utils.ai_moderator import quick_crisis_check
        if quick_crisis_check(text):
            post.show_crisis_resources = True
            logger.info("Crisis keywords detected - showing resources immediately")

        # Phase 2: Full AI moderation runs async after post is saved
        # This is handled in save() method after commit
