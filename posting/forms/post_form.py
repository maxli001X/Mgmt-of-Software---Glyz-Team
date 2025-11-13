from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "tags", "is_anonymous")
        widgets = {
            "tags": forms.CheckboxSelectMultiple,
            "body": forms.Textarea(attrs={"rows": 4}),
        }

    def save(self, commit=True, author=None):
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()
            self.save_m2m()
        return post

