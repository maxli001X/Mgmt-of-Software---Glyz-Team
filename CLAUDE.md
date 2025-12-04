# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tree Hole Yale is an anonymous Yale-only campus forum built with Django. Users can post anonymously, react to posts (upvote/downvote), flag content for moderation, and filter by tags.

**Live**: https://glyz-team-tlug.onrender.com

## Development Commands

```bash
# Activate virtual environment and run server
source venv/bin/activate
python manage.py runserver

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test posting
python manage.py test posting.tests.test_feed

# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Check for issues
python manage.py check
```

## Architecture

### Django Apps

| App | Purpose | URL Prefix |
|-----|---------|------------|
| `posting/` | Main forum (posts, tags, voting) | `/` |
| `auth_landing/` | Login, signup, logout | `/auth/` |
| `moderation_ranking/` | Moderator dashboard | `/moderation/` |
| `profile_settings/` | User profiles | `/profile/` |
| `analytics/` | A/B test endpoint | `/972b69d/` |

### Feature-Based File Organization

The `posting` app uses **feature-based organization** to minimize merge conflicts:

```
posting/
├── models/
│   ├── post.py      # Post model
│   ├── tag.py       # Tag model
│   ├── vote.py      # Vote model
│   └── __init__.py  # Exports: Post, Tag, Vote
├── views/
│   ├── feed.py          # Home feed, tag filtering
│   ├── post_actions.py  # upvote_post, downvote_post, flag_post
│   ├── user_stats.py    # my_stats, admin_user_list, aggregated_stats
│   └── __init__.py      # Exports all views
├── forms/
│   └── post_form.py
└── tests/
    ├── test_models.py
    ├── test_forms.py
    ├── test_feed.py
    └── test_post_actions.py
```

**Key pattern**: Each feature gets its own file. New models/views/forms go in separate files, then export via `__init__.py`.

### Authentication

- Email restricted to `@yale.edu` addresses (configurable via `ALLOWED_EMAIL_DOMAINS`)
- Yale email validation in `auth_landing/forms.py:YaleSignUpForm`
- Login redirects to `posting:home`, logout to `auth_landing:landing`

### Configuration

Settings in `treehole/settings.py` use `python-decouple` for environment variables:

- `DJANGO_SECRET_KEY` - Secret key (required in production)
- `DJANGO_DEBUG` - Debug mode (default: True)
- `DATABASE_URL` - PostgreSQL connection string (falls back to SQLite)
- `ALLOWED_EMAIL_DOMAINS` - Comma-separated email domains (default: yale.edu)
- `DJANGO_ALLOWED_HOSTS` - Allowed hosts
- `DJANGO_CSRF_TRUSTED_ORIGINS` - CSRF trusted origins

### Static Files

WhiteNoise serves static files. Run `python manage.py collectstatic` if CSS/JS changes aren't appearing.

## Git Workflow

Branch naming: `feature/description-XX`, `fix/description-XX`, `refactor/description-XX` (XX = issue number)

Commit format: `<type>: <description> (#issue-number)` where type is `feat`, `fix`, `test`, `refactor`, or `docs`

## Testing

Tests live in `<app>/tests/` directory. Each test file focuses on one area (models, forms, views, specific features).
