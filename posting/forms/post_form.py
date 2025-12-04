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
            "is_anonymous": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
        labels = {
            "title": "Title",
            "body": "Post Content",
            "is_anonymous": "Post anonymously",
        }
    
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

        # Run AI content moderation before saving
        self._run_ai_moderation(post)

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

        return post

    def _run_ai_moderation(self, post):
        """
        Run AI content moderation on the post.

        Sets ai_flagged, ai_severity_score, ai_categories, and show_crisis_resources.
        """
        try:
            from ..utils.ai_moderator import get_moderator

            moderator = get_moderator()
            text = f"{post.title}\n\n{post.body}"
            result = moderator.check_content(text)

            post.ai_flagged = result.get("flagged", False)
            post.ai_severity_score = result.get("severity_score")
            post.ai_categories = result.get("category_scores")
            post.show_crisis_resources = result.get("is_crisis", False)

            # Auto-flag for human review if AI flags it
            if post.ai_flagged:
                post.is_flagged = True

        except Exception:
            # If AI moderation fails, continue without it
            pass
