from django import forms

from ..models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating comments on posts."""

    class Meta:
        model = Comment
        fields = ("body", "is_anonymous")
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-textarea comment-textarea",
                    "placeholder": "Add a comment...",
                    "aria-label": "Comment text",
                }
            ),
            "is_anonymous": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }
        labels = {
            "body": "Comment",
            "is_anonymous": "Post anonymously",
        }

    def __init__(self, *args, **kwargs):
        # Accept post and parent_comment but don't add to form fields
        self.post = kwargs.pop("post", None)
        self.parent_comment = kwargs.pop("parent_comment", None)
        super().__init__(*args, **kwargs)

    def clean_body(self):
        """Ensure comment body is not empty or just whitespace."""
        body = self.cleaned_data.get("body", "").strip()
        if not body:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(body) < 2:
            raise forms.ValidationError("Comment must be at least 2 characters.")
        if len(body) > 5000:
            raise forms.ValidationError("Comment must be less than 5000 characters.")
        return body

    def save(self, commit=True, author=None):
        """Save comment with post, parent, and author."""
        comment = super().save(commit=False)

        if author is not None:
            comment.author = author

        if self.post is not None:
            comment.post = self.post

        if self.parent_comment is not None:
            comment.parent_comment = self.parent_comment

        # Run AI content moderation before saving
        self._run_ai_moderation(comment)

        if commit:
            comment.save()

        return comment

    def _run_ai_moderation(self, comment):
        """
        Run AI content moderation on the comment.

        Sets ai_flagged, ai_severity_score, ai_categories, and show_crisis_resources.
        """
        try:
            from ..utils.ai_moderator import get_moderator

            moderator = get_moderator()
            result = moderator.check_content(comment.body)

            comment.ai_flagged = result.get("flagged", False)
            comment.ai_severity_score = result.get("severity_score")
            comment.ai_categories = result.get("category_scores")
            comment.show_crisis_resources = result.get("is_crisis", False)

            # Auto-flag for human review if AI flags it
            if comment.ai_flagged:
                comment.is_flagged = True

        except Exception:
            # If AI moderation fails, continue without it
            pass
