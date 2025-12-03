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
        """Clean and normalize tag input."""
        tags_input = self.cleaned_data.get("tags_input", "").strip()
        
        if tags_input:
            # Validate individual tags
            for tag in tags_input.split(","):
                tag = tag.strip().lstrip("#").strip()
                if tag:
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
        """Get or create a tag by name."""
        tag_name = tag_name.strip().lower()
        if not tag_name:
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
