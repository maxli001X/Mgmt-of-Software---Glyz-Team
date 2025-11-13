# Tree Hole Yale – File Guide

Plain-English map of the important files and what they do. Skim this whenever you wonder “what is this file for?”

## Root Level

- `manage.py` — Django command runner (`python manage.py runserver`, `migrate`, etc.).
- `requirements.txt` — Python packages the app needs; Render uses this to install dependencies.
- `Procfile` — Render/Gunicorn start command (`web: gunicorn treehole.wsgi:application`).
- `render.yaml` — Render “blueprint” to spin up the web app + PostgreSQL database automatically.
- `env.example` — Template of environment variables; copy to `.env` and fill in secrets (already done).
- `.env` (ignored by git) — Actual secrets and database settings Django reads at runtime.
- `README.md` — High-level setup + deployment instructions.
- `FILE_GUIDE.md` — This file.

## Project Package (`treehole/`)

- `treehole/settings.py` — Main Django configuration (apps to load, database info, static files, etc.).
- `treehole/urls.py` — Maps incoming URLs to app-specific URL configs.
- `treehole/wsgi.py` — WSGI entry point used by Gunicorn/Render for production.
- `treehole/asgi.py` — ASGI entry point (future-proofing for async/websockets).
- `treehole/__init__.py` — Marks this folder as a Python package.

## Auth Landing App (`auth_landing/`)

- `auth_landing/forms.py` — Yale-only signup form validation.
- `auth_landing/views.py` — Signup, login, logout views.
- `auth_landing/urls.py` — Routes `/auth/signup/`, `/auth/login/`, `/auth/logout/`.
- `auth_landing/tests.py` — Smoke tests covering the signup flow.
- Templates live under `templates/auth_landing/`.

## Posting App (`posting/`)

**Feature-based structure for parallel development:**

- `posting/models/` — Models organized by feature:
  - `tag.py` — Tag model
  - `post.py` — Post model
  - `vote.py` — Vote model
  - `__init__.py` — Exports all models for backward compatibility
- `posting/forms/` — Forms organized by feature:
  - `post_form.py` — PostForm for creating posts
  - `__init__.py` — Exports all forms
- `posting/views/` — Views organized by feature:
  - `feed.py` — Home feed view with tag filtering
  - `post_actions.py` — Upvote and flag actions
  - `__init__.py` — Exports all views
- `posting/tests/` — Tests organized by feature:
  - `test_models.py` — Model tests
  - `test_forms.py` — Form submission tests
  - `test_feed.py` — Feed view tests
  - `test_post_actions.py` — Voting/flagging tests
  - `__init__.py` — Test discovery
- `posting/urls.py` — Feed + action routes (`/`, `/posts/<id>/...`).
- `posting/admin.py` — Admin configuration for moderator review.
- Templates live under `templates/posting/` with:
  - `home.html` — Main feed page
  - `components/` — Reusable components (for future refactoring)
  - `includes/` — Template includes

## Moderation Ranking App (`moderation_ranking/`)

**Structured for moderation features (story #50):**

- `moderation_ranking/views/` — Moderation views:
  - `dashboard.py` — Moderation dashboard view
  - `__init__.py` — Exports all views
- `moderation_ranking/urls.py` — Moderation routes
- `moderation_ranking/tests.py` — Moderation tests
- Templates live under `templates/moderation_ranking/`:
  - `dashboard.html` — Main moderation dashboard
  - `components/` — Reusable moderation components (for future)

## Profile Settings App (`profile_settings/`)

**Structured for profile features (stories #43–#45):**

- `profile_settings/models/` — Profile models (placeholders):
  - `user_profile.py` — UserProfile model (to be implemented)
  - `__init__.py` — Model exports
- `profile_settings/views/` — Profile views:
  - `profile.py` — Profile dashboard view
  - `__init__.py` — Exports all views
- `profile_settings/forms/` — Profile forms (placeholders):
  - `profile_form.py` — Profile forms (to be implemented)
  - `__init__.py` — Form exports
- `profile_settings/urls.py` — Profile routes
- `profile_settings/tests.py` — Profile tests
- Templates live under `templates/profile_settings/dashboard.html`

## Templates (`templates/`)

- `templates/base.html` — Master layout, navigation, shared messages.
- `templates/auth_landing/` — Login, signup, logout screens.
- `templates/posting/home.html` — Posting feed with composer, tags, upvote/flag buttons.
- `templates/moderation_ranking/dashboard.html` — Moderator placeholder.
- `templates/profile_settings/dashboard.html` — Profile/settings placeholder.

## Static Assets (`static/`)

- `static/css/styles.css` — Global styling (colors, layout, typography).
- `.gitkeep` files — Empty placeholders so git keeps the folders even when empty.

## Media (`media/`)

- Placeholder for user-uploaded files (currently unused but wired up for future features).

## Virtual Environment (`venv/`)

- Python interpreter + installed packages for local development. Not checked into git but kept locally.

---

## Issue Mapping

- `ISSUE_STORY_MAPPING.md` — Cross-reference between GitHub issues (#39–#50) and the files that satisfy each story/epic.

