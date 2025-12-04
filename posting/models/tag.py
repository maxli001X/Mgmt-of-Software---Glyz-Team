from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    """Tag model for categorizing posts.

    Tag names must:
    - Be 2-50 characters long
    - Not contain '#' symbols
    - Not contain spaces
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        """Validate tag name constraints."""
        super().clean()
        if self.name:
            if '#' in self.name:
                raise ValidationError({"name": "Tag name cannot contain '#' symbol."})
            if ' ' in self.name:
                raise ValidationError({"name": "Tag name cannot contain spaces."})
            if len(self.name) < 2:
                raise ValidationError({"name": "Tag name must be at least 2 characters."})

    def save(self, *args, **kwargs):
        """Save with validation."""
        self.full_clean()
        super().save(*args, **kwargs)

