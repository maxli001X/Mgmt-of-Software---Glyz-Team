# Tree Hole Yale

Tree Hole Yale is an anonymous, Yale-only campus forum inspired by SideChat. Students can speak freely, react to posts, and flag content for moderation while keeping their identity private.

- Repository: https://github.com/doriru89/Mgmt-of-Software---Glyz-Team
- Render ready: `Procfile`, `render.yaml`, and pip-based build are configured; connect the repo in Render to deploy.
- Story ↔ code reference: see `ISSUE_STORY_MAPPING.md` for how each GitHub story maps to files.

## Tech Stack

- Django 5 + Python 3.12 (virtualenv already provisioned in `venv/`)
- PostgreSQL (Render managed database in production)
- WhiteNoise for static files in production

---

## 1. Local Environment Setup

1. **Activate the virtual environment**

   ```bash
   cd "/Users/hey/Documents/Cursor Projects/Tree Hole Yale"
   source venv/bin/activate
   ```

2. **Install dependencies** (already installed, but re-run after future updates):

   ```bash
   pip install -r requirements.txt
   ```

3. **Copy environment variables template**

   ```bash
   cp env.example .env
   ```

   Fill in a long random string for `DJANGO_SECRET_KEY`. Start with SQLite locally, then switch to PostgreSQL when ready.

---

## 2. Database Options

### Option A: Quick Start with SQLite (local dev)

1. Keep `DB_ENGINE=django.db.backends.sqlite3` in `.env`.
2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Start the dev server:

   ```bash
   python manage.py runserver
   ```

### Option B: PostgreSQL on macOS

1. Install PostgreSQL:
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. Create database + user:
   ```bash
   createuser treehole --pwprompt
   createdb treehole --owner treehole
   ```

3. Update `.env` (either `DATABASE_URL=postgresql://treehole:<password>@localhost:5432/treehole` or explicit fields).
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

### Option C: Render Managed PostgreSQL

1. In Render, click **New > PostgreSQL** database.
2. Copy the `External Database URL`; set it as `DATABASE_URL` in Render and `.env`.
3. Ensure `DB_SSL_REQUIRE=True` when using Render (set in Django environment variables).

---

## 3. Django Admin & Authentication

1. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```
2. Default auth is standard Django login (`/admin/`). In the next section (`auth-flow`) we will add Yale-only email validation/SSO guidance.

### Yale-specific signup flow

- Users register via `/auth/signup/`. Only emails ending with `@yale.edu` (configurable via `ALLOWED_EMAIL_DOMAINS` in your `.env`) are accepted.
- Successful signups are automatically logged in and redirected to the posting feed.
- Auth screens now live in the `auth_landing` app (`auth_landing/forms.py`, `auth_landing/views.py`, templates under `templates/auth_landing/`).

---

## 4. Deployment (Render)

**📘 For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

### Quick Start with Blueprint (Recommended)

The repository includes a Render blueprint (`render.yaml`) that provisions a web service and a managed PostgreSQL database in one click.

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. In Render Dashboard:
   - Go to **New > Blueprint**
   - Connect your GitHub repository
   - Select this repository
   - Review the configuration
   - Click **Apply**

3. Render will automatically:
   - Create PostgreSQL database (`glyz-team-db`)
   - Deploy web service (`glyz-team`)
   - Generate a secure `DJANGO_SECRET_KEY`
   - Configure all environment variables
   - Run migrations and collect static files
   - Start the application

4. Your app will be live at: `https://glyz-team.onrender.com`

5. Create a superuser (via Render Dashboard → Shell):
   ```bash
   python manage.py createsuperuser
   ```

### Key Configuration Files

- `render.yaml` - Blueprint specification (web service + database)
- `runtime.txt` - Python version (3.12.0)
- `.renderignore` - Files to exclude from deployment
- `build.sh` - Optional build script
- `Procfile` - Process type definition

### Environment Variables (Auto-Configured)

All required environment variables are defined in `render.yaml`:
- `DJANGO_SECRET_KEY` (auto-generated)
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_DEBUG=False`
- `DATABASE_URL` (from managed PostgreSQL)
- `ALLOWED_EMAIL_DOMAINS=yale.edu`

### Static Files

WhiteNoise is preconfigured; no extra Render storage needed.

## 5. Project Structure

```
Tree Hole Yale/
├── env.example
├── manage.py
├── auth_landing/        # Authentication landing screens (Sign in/up/out)
├── posting/             # Posting feed, tag filtering, upvotes/flags (forum epic)
├── moderation_ranking/  # Placeholder app for moderator ranking dashboards
├── profile_settings/    # Placeholder app for profile & settings stories
├── treehole/            # Project settings, URLs, ASGI/WSGI
├── templates/           # Base templates + per-app screen templates
├── static/              # Static assets (add CSS/JS here)
├── media/               # User-uploaded media (optional)
├── requirements.txt
└── venv/                # Virtualenv (kept locally, not pushed)
```

---

## 6. Next Steps

- Populate the moderation dashboard (`moderation_ranking`) and profile/settings screens (`profile_settings`) to complete stories #43–#50.
- Harden anonymous posting (rate limiting, deletion, admin tooling).
- Integrate Yale SSO once requirements/policies are finalized.
- Expand automated tests (see `posting/tests.py`, `auth_landing/tests.py`, etc. for starting points).

## 7. Testing & QA

- Run `python manage.py test` regularly as you add features.
- Use `python manage.py runserver` locally and navigate to `http://127.0.0.1:8000/` to test the posting flow.
- For integration testing, seed sample tags via the Django admin and ensure filtering works.
- Before each Render deploy, run `python manage.py collectstatic` locally to verify assets build.

### Production security defaults

- With `DJANGO_DEBUG=False`, cookies are marked `Secure`, HTTPS redirects are enforced, and HSTS defaults to one year. Override via:
  - `DJANGO_SESSION_COOKIE_SECURE`, `DJANGO_CSRF_COOKIE_SECURE`
  - `DJANGO_SESSION_COOKIE_SAMESITE`, `DJANGO_CSRF_COOKIE_SAMESITE`
  - `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_HSTS_SECONDS`, `DJANGO_HSTS_INCLUDE_SUBDOMAINS`, `DJANGO_HSTS_PRELOAD`
- A stricter referrer policy (`strict-origin`) and `X_FRAME_OPTIONS=DENY` are enabled by default; override via `DJANGO_SECURE_REFERRER_POLICY` or `DJANGO_X_FRAME_OPTIONS` if you embed the app elsewhere.

> **Heads up:** if you previously migrated the old `forum`/`accounts` apps, clear your local database (`rm db.sqlite3 && python manage.py migrate`) to sync with the new app layout.

