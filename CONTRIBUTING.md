# Team Collaboration Guide

How to work together on Tree Hole Yale without merge conflicts.

---

## Project Structure

```
Tree Hole Yale/
├── auth_landing/          # Login, signup, logout
│   ├── forms.py           # Yale email validation
│   ├── views.py           # Auth views
│   └── urls.py            # /auth/* routes
│
├── posting/               # Main forum features
│   ├── models/            # Feature-based models
│   │   ├── post.py        # Post model
│   │   ├── tag.py         # Tag model
│   │   ├── vote.py        # Vote model
│   │   └── __init__.py    # Export all models
│   ├── views/             # Feature-based views
│   │   ├── feed.py        # Home feed with tag filtering
│   │   ├── post_actions.py # Upvote, flag actions
│   │   └── __init__.py    # Export all views
│   ├── forms/             # Feature-based forms
│   │   ├── post_form.py   # Post creation form
│   │   └── __init__.py    # Export all forms
│   ├── tests/             # Feature-based tests
│   │   ├── test_models.py
│   │   ├── test_forms.py
│   │   ├── test_feed.py
│   │   ├── test_post_actions.py
│   │   └── __init__.py
│   └── urls.py            # /posts/* routes
│
├── moderation_ranking/    # Moderation features
│   ├── views/
│   │   └── dashboard.py   # Moderator dashboard
│   └── urls.py            # /moderation/* routes
│
├── profile_settings/      # User profile features (in development)
│   ├── models/
│   │   └── user_profile.py
│   ├── views/
│   │   └── profile.py
│   └── urls.py            # /profile/* routes
│
├── templates/             # HTML templates
│   ├── base.html          # Base layout (navigation, messages)
│   ├── auth_landing/      # Auth pages
│   ├── posting/           # Feed and post pages
│   ├── moderation_ranking/
│   └── profile_settings/
│
└── static/                # CSS, JS, images
    └── css/
        └── styles.css     # Global styles
```

---

## Understanding the Structure

Django projects have 3 types of folders:

### 1. Project Configuration (`treehole/`)
**Purpose**: Controls how Django runs  
**What's inside**: Settings, master URL routing, server config  
**You rarely touch this** unless adding new apps or changing settings

### 2. HTML Templates (`templates/`)
**Purpose**: HTML pages users see  
**What's inside**: Login forms, feed pages, dashboards  
**Django convention**: Always called `templates/`

### 3. App Folders (`posting/`, `auth_landing/`, etc.)
**Purpose**: Business logic for features  
**What's inside**: Models, views, forms, tests  
**This is where you work** when adding features

---

## Design Philosophy: Feature-Based Organization

**Each feature gets its own file** to minimize merge conflicts.

### ✅ Good (Multiple developers can work in parallel)
```
posting/models/
├── post.py          ← Developer A working here
├── comment.py       ← Developer B working here
└── notification.py  ← Developer C working here
```

### ❌ Bad (Everyone editing same file = conflicts)
```
posting/
└── models.py  ← All 3 developers editing this!
```

---

## Git Workflow

### 1. Pick a Task
- Check GitHub Issues for open stories
- Comment that you're working on it
- Note the issue number (e.g., #51)

### 2. Create Feature Branch
```bash
git checkout -b feature/add-comments-51
```

**Branch naming:**
- `feature/description-XX` (new feature)
- `fix/description-XX` (bug fix)
- `refactor/description-XX` (code improvement)

### 3. Work on Your Feature
Make small, focused commits:
```bash
git add posting/models/comment.py
git commit -m "feat: Add Comment model (#51)"

git add posting/views/comments.py
git commit -m "feat: Add comment view (#51)"

git add posting/tests/test_comments.py
git commit -m "test: Add comment tests (#51)"
```

**Commit message format:**
```
<type>: <description> (#issue-number)

Types: feat, fix, test, refactor, docs
```

### 4. Keep Branch Updated
```bash
git fetch origin
git rebase origin/main
```

If conflicts occur, resolve them and continue:
```bash
# Fix conflicts in your editor
git add .
git rebase --continue
```

### 5. Push and Create Pull Request
```bash
git push origin feature/add-comments-51
```

On GitHub:
1. Create Pull Request
2. Reference issue: "Closes #51"
3. Describe changes
4. Request review from teammate

### 6. After PR is Merged
```bash
git checkout main
git pull origin main
git branch -d feature/add-comments-51  # Delete local branch
```

---

## Adding a Feature (Example: Comment System)

### Step 1: Create Model
```python
# posting/models/comment.py
from django.conf import settings
from django.db import models
from .post import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
```

### Step 2: Export Model
```python
# posting/models/__init__.py
from .comment import Comment  # Add this line
from .post import Post
from .tag import Tag
from .vote import Vote

__all__ = ["Post", "Tag", "Vote", "Comment"]
```

### Step 3: Create Form
```python
# posting/forms/comment_form.py
from django import forms
from ..models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body", "is_anonymous")
```

Export in `posting/forms/__init__.py`.

### Step 4: Create View
```python
# posting/views/comments.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

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
    return redirect("posting:home")
```

Export in `posting/views/__init__.py`.

### Step 5: Add URL
```python
# posting/urls.py
from django.urls import path
from . import views

app_name = "posting"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<int:pk>/upvote/", views.upvote_post, name="upvote"),
    path("posts/<int:pk>/flag/", views.flag_post, name="flag"),
    path("posts/<int:post_pk>/comment/", views.add_comment, name="add_comment"),  # Add
]
```

### Step 6: Create Tests
```python
# posting/tests/test_comments.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Comment, Post, Tag

class CommentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", email="test@yale.edu", password="pass"
        )
        self.tag = Tag.objects.create(name="Test", slug="test")
        self.post = Post.objects.create(title="Test", body="Body", author=self.user)

    def test_add_comment(self):
        self.client.login(username="test", password="pass")
        response = self.client.post(
            f"/posts/{self.post.pk}/comment/",
            {"body": "Test comment", "is_anonymous": True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(body="Test comment").exists())
```

Export in `posting/tests/__init__.py`.

### Step 7: Migrate & Test
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test posting.tests.test_comments
```

---

## Issue → Code Location

| Issue | Feature | Where to Add |
|-------|---------|--------------|
| #39-40 | Authentication | `auth_landing/` |
| #41 | Tag Filtering | `posting/views/feed.py`, `posting/models/tag.py` |
| #42 | Post Composer | `posting/forms/post_form.py`, `posting/views/feed.py` |
| #43-45 | Profile & Settings | `profile_settings/models/`, `profile_settings/views/` |
| #46 | Design System | `templates/base.html`, `static/css/styles.css` |
| #48-49 | Voting & Flagging | `posting/views/post_actions.py`, `posting/models/vote.py` |
| #50 | Moderation | `moderation_ranking/views/`, `posting/admin.py` |

---

## Avoiding Merge Conflicts

### Scenario 1: Two Developers, Different Features

**Developer A**: Adding comments (#51)
- Creates `posting/models/comment.py`
- Creates `posting/views/comments.py`
- Creates `posting/forms/comment_form.py`

**Developer B**: Adding notifications (#52)
- Creates `posting/models/notification.py`
- Creates `posting/views/notifications.py`

**Result**: ✅ No conflicts! Different files.

### Scenario 2: Conflicts in `__init__.py`

**Developer A** adds to `posting/models/__init__.py`:
```python
from .comment import Comment
```

**Developer B** adds to `posting/models/__init__.py`:
```python
from .notification import Notification
```

**Conflict!** Both modified `__init__.py`.

**Resolution** (simple):
```python
from .comment import Comment
from .notification import Notification
from .post import Post
from .tag import Tag
from .vote import Vote

__all__ = ["Post", "Tag", "Vote", "Comment", "Notification"]
```

**Tip**: Commit `__init__.py` changes separately to make merging easier.

---

## Pull Request Checklist

Before creating PR:
- [ ] Tests pass: `python manage.py test`
- [ ] Code follows project structure
- [ ] New models exported in `__init__.py`
- [ ] New views exported in `__init__.py`
- [ ] URLs added/updated
- [ ] Tests added for new features
- [ ] Commit messages reference issue number
- [ ] Branch is up-to-date with main

---

## Communication Tips

### Before Starting Work
- Check if someone is already working on the issue
- Comment on the issue that you're taking it
- Coordinate with team if working on related features

### During Development
- Push your branch regularly (even if incomplete)
- Update issue with progress
- Ask for help if stuck

### Code Review
- Review teammate's PRs promptly
- Be constructive in feedback
- Test their changes locally before approving

---

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test posting

# Run specific file
python manage.py test posting.tests.test_comments
```

Always run tests before pushing!

---

## Quick Reference

```bash
# Start work on new feature
git checkout main
git pull origin main
git checkout -b feature/my-feature-XX

# Save progress
git add .
git commit -m "feat: Description (#XX)"
git push origin feature/my-feature-XX

# Update your branch with latest main
git fetch origin
git rebase origin/main

# After PR merged
git checkout main
git pull origin main
git branch -d feature/my-feature-XX
```

---

## Summary

**Key Principles for Collaboration:**
1. **One feature = One set of new files** (not editing shared files)
2. **Small, focused commits** with clear messages
3. **Reference issue numbers** in commits and PRs
4. **Test before pushing**
5. **Keep branch updated** with main
6. **Communicate** with team

Following this workflow minimizes conflicts and keeps development smooth! 🚀
