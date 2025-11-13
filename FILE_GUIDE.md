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

- `posting/models.py` — Post/Tag/Vote models backing the feed.
- `posting/forms.py` — Anonymous post form.
- `posting/views.py` — Feed, tag filtering, upvote/flag handlers.
- `posting/urls.py` — Feed + action routes (`/`, `/posts/<id>/...`).
- `posting/admin.py` — Admin configuration for moderator review.
- `posting/tests.py` — View + form smoke tests.
- Templates live under `templates/posting/`.

## Moderation Ranking App (`moderation_ranking/`)

- Placeholder screen for future moderation tooling (story #50).
- `moderation_ranking/views.py`, `urls.py`, `tests.py`, and template `templates/moderation_ranking/dashboard.html`.

## Profile Settings App (`profile_settings/`)

- Placeholder screen for profile and settings stories (#43–#45).
- `profile_settings/views.py`, `urls.py`, `tests.py`, and template `templates/profile_settings/dashboard.html`.

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

