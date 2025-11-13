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

## Forum App (`forum/`)

- `forum/models.py` — Database tables defined in Python (`Post`, `Tag`, `Vote`).
- `forum/forms.py` — HTML form logic for creating posts.
- `forum/views.py` — Functions that handle page requests (home feed, upvote, flag).
- `forum/urls.py` — URL patterns for forum features (`/`, `/posts/<id>/upvote/`, etc.).
- `forum/admin.py` — Registers models so staff can manage them via `/admin/`.
- `forum/migrations/` — Auto-generated files that build the database schema for the forum.

## Accounts App (`accounts/`)

- `accounts/forms.py` — Signup form that enforces `@yale.edu` email addresses.
- `accounts/views.py` — Login, logout, signup page logic.
- `accounts/urls.py` — Routes `/accounts/login/`, `/accounts/signup/`, `/accounts/logout/`.
- `accounts/admin.py`, `accounts/models.py`, etc. — Defaults from Django; currently minimal but ready for customization.

## Templates (`templates/`)

- `templates/base.html` — Master layout (nav bar, messages, loads CSS); all other templates extend this.
- `templates/forum/home.html` — Homepage feed, post submission form, filtering by tags.
- `templates/accounts/login.html` — Login page.
- `templates/accounts/signup.html` — Signup page.
- `templates/accounts/logout.html` — Logout confirmation page.

## Static Assets (`static/`)

- `static/css/styles.css` — Global styling (colors, layout, typography).
- `.gitkeep` files — Empty placeholders so git keeps the folders even when empty.

## Media (`media/`)

- Placeholder for user-uploaded files (currently unused but wired up for future features).

## Virtual Environment (`venv/`)

- Python interpreter + installed packages for local development. Not checked into git but kept locally.

