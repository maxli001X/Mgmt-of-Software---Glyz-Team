# Development Workflow Guide

This guide explains how to work on user stories in the Tree Hole Yale project without causing merge conflicts with other developers.

## Project Structure Philosophy

The codebase is organized by **feature**, not by file type. This means:
- Multiple developers can work on different features simultaneously
- Each feature has its own files (models, views, forms, tests)
- Merge conflicts are minimized because you're rarely editing the same files

## Adding a New Feature (Step-by-Step)

### Example: Adding a Comment System (#Story #51)

#### 1. **Create the Model** (`posting/models/comment.py`)

```python
from django.conf import settings
from django.db import models

from .post import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    body = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
```

#### 2. **Export the Model** (Update `posting/models/__init__.py`)

```python
from .comment import Comment  # Add this line
from .post import Post
from .tag import Tag
from .vote import Vote

__all__ = ["Post", "Tag", "Vote", "Comment"]  # Add "Comment"
```

#### 3. **Create the Form** (`posting/forms/comment_form.py`)

```python
from django import forms
from ..models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body", "is_anonymous")
```

#### 4. **Export the Form** (Update `posting/forms/__init__.py`)

```python
from .comment_form import CommentForm  # Add this line
from .post_form import PostForm

__all__ = ["PostForm", "CommentForm"]  # Add "CommentForm"
```

#### 5. **Create the View** (`posting/views/comments.py`)

```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from ..forms import CommentForm
from ..models import Post


@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added!")
    return redirect(reverse("posting:home"))
```

#### 6. **Export the View** (Update `posting/views/__init__.py`)

```python
from .comments import add_comment  # Add this line
from .feed import home
from .post_actions import flag_post, upvote_post

__all__ = ["home", "upvote_post", "flag_post", "add_comment"]  # Add "add_comment"
```

#### 7. **Add the URL Route** (Update `posting/urls.py`)

```python
from django.urls import path

from . import views

app_name = "posting"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<int:pk>/upvote/", views.upvote_post, name="upvote"),
    path("posts/<int:pk>/flag/", views.flag_post, name="flag"),
    path("posts/<int:post_pk>/comment/", views.add_comment, name="add_comment"),  # Add this
]
```

#### 8. **Create Tests** (`posting/tests/test_comments.py`)

```python
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Comment, Post, Tag


class CommentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="commenter",
            email="commenter@yale.edu",
            password="password123",
        )
        self.tag = Tag.objects.create(name="General", slug="general")
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            author=self.user,
        )

    def test_add_comment_requires_auth(self):
        response = self.client.post(
            reverse("posting:add_comment", kwargs={"post_pk": self.post.pk}),
            data={"body": "Test comment", "is_anonymous": True},
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_authenticated_comment_submission(self):
        self.client.login(username="commenter", password="password123")
        response = self.client.post(
            reverse("posting:add_comment", kwargs={"post_pk": self.post.pk}),
            data={"body": "Test comment", "is_anonymous": True},
        )
        self.assertEqual(response.status_code, 302)  # Redirect to feed
        self.assertTrue(Comment.objects.filter(body="Test comment").exists())
```

#### 9. **Update Tests __init__.py** (`posting/tests/__init__.py`)

```python
from .test_comments import *  # noqa - Add this line
from .test_feed import *  # noqa
from .test_forms import *  # noqa
from .test_models import *  # noqa
from .test_post_actions import *  # noqa
```

#### 10. **Create Database Migration**

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 11. **Update Template** (`templates/posting/home.html`)

Add a comments section to display and submit comments for each post.

---

## Where to Add Different Types of Features

### Authentication Features (Stories #39-40, #47)
- **App:** `auth_landing/`
- **Models:** Use Django's built-in User model
- **Views:** Add to `auth_landing/views.py`
- **Forms:** Add to `auth_landing/forms.py`
- **Templates:** `templates/auth_landing/`
- **URLs:** `auth_landing/urls.py`

### Feed & Posting Features (Stories #41-42, #48-49)
- **App:** `posting/`
- **Models:** Add to `posting/models/` (new file per model)
- **Views:** Add to `posting/views/` (new file per feature)
- **Forms:** Add to `posting/forms/` (new file per form)
- **Tests:** Add to `posting/tests/` (new file per feature)
- **Templates:** `templates/posting/`
- **URLs:** `posting/urls.py`

### Profile & Settings Features (Stories #43-45)
- **App:** `profile_settings/`
- **Models:** Add to `profile_settings/models/` (currently has placeholders)
- **Views:** Add to `profile_settings/views/` (currently has dashboard stub)
- **Forms:** Add to `profile_settings/forms/` (currently empty)
- **Tests:** Add to `profile_settings/tests.py`
- **Templates:** `templates/profile_settings/`
- **URLs:** `profile_settings/urls.py`

### Moderation Features (Story #50)
- **App:** `moderation_ranking/`
- **Models:** Add to `moderation_ranking/models.py`
- **Views:** Add to `moderation_ranking/views/` (currently has dashboard stub)
- **Templates:** `templates/moderation_ranking/` with `components/` for reusable parts
- **URLs:** `moderation_ranking/urls.py`

### Shared Components (Story #46)
- **Base Layout:** `templates/base.html`
- **CSS:** `static/css/styles.css`
- **JavaScript:** `static/js/` (create if needed)

---

## Git Workflow Best Practices

### 1. **Create a Feature Branch**
```bash
git checkout -b feature/comments-story-51
```

### 2. **Make Small, Focused Commits**
```bash
git add posting/models/comment.py posting/models/__init__.py
git commit -m "Add Comment model for story #51"

git add posting/forms/comment_form.py posting/forms/__init__.py
git commit -m "Add CommentForm for story #51"

git add posting/views/comments.py posting/views/__init__.py
git commit -m "Add add_comment view for story #51"

git add posting/urls.py
git commit -m "Add comment route for story #51"

git add posting/tests/test_comments.py posting/tests/__init__.py
git commit -m "Add comment tests for story #51"
```

### 3. **Push and Create Pull Request**
```bash
git push origin feature/comments-story-51
```
Then create a PR on GitHub referencing the story number (#51).

### 4. **Keep Branch Updated**
```bash
git fetch origin
git rebase origin/main
```

---

## Common Scenarios

### Scenario 1: Two Developers Working on Different Features
**Developer A:** Adding comments (Story #51)
- Creates `posting/models/comment.py`
- Creates `posting/views/comments.py`
- Creates `posting/forms/comment_form.py`
- Creates `posting/tests/test_comments.py`

**Developer B:** Adding trending feed (Story #52)
- Creates `posting/views/trending.py`
- Creates `templates/posting/trending.html`
- Creates `posting/tests/test_trending.py`

**Result:** ✅ No conflicts! They're working in different files.

### Scenario 2: Two Developers Need to Update Same __init__.py
**Developer A:** Adds `Comment` to `posting/models/__init__.py`
```python
from .comment import Comment
```

**Developer B:** Adds `Reaction` to `posting/models/__init__.py`
```python
from .reaction import Reaction
```

**Result:** ⚠️ Merge conflict in `__init__.py`, but it's simple to resolve:
```python
from .comment import Comment
from .reaction import Reaction
```

**Tip:** Keep `__init__.py` changes in separate commits to make merging easier.

---

## Testing Your Changes

### Run All Tests
```bash
python manage.py test
```

### Run Tests for Specific App
```bash
python manage.py test posting
```

### Run Tests for Specific Feature
```bash
python manage.py test posting.tests.test_comments
```

### Check for Issues
```bash
python manage.py check
```

---

## Summary: Key Principles

1. **One feature = One set of new files** - Avoid editing existing feature files when possible
2. **Use feature-based naming** - `comments.py`, `trending.py`, not `views.py`
3. **Keep __init__.py updates minimal** - Just add your imports
4. **Test early and often** - Run `python manage.py check` and tests frequently
5. **Small commits** - Easier to review and merge
6. **Reference story numbers** - Always mention the story # in commits and PRs

---

## Need Help?

- **File structure unclear?** Check `FILE_GUIDE.md`
- **Which files to edit?** Check `ISSUE_STORY_MAPPING.md`
- **Code not working?** Run `python manage.py check` first
- **Tests failing?** Run `python manage.py test` to see what broke

Happy coding! 🚀

