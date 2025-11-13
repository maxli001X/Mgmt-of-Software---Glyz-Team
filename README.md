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

### Option A: Blueprint (recommended)

The repository includes a Render blueprint (`render.yaml`) that provisions a web service and a managed PostgreSQL database in one click.

1. In Render, go to **Blueprints > New Blueprint Instance** and select this repo/branch.
2. Review the plan (web service on the free plan + free Postgres) and click **Apply**.
3. When prompted, add secrets tagged `sync: false`:
   - `DJANGO_SECRET_KEY` – paste a long random string.
4. Optionally adjust:
   - `DJANGO_ALLOWED_HOSTS` – include additional custom domains if you add them later.
   - `DJANGO_CSRF_TRUSTED_ORIGINS` – include the same hosts prefixed with `https://`.
5. Deploy. The blueprint runs these stages automatically:
   - `pip install -r requirements.txt`
   - `python manage.py collectstatic --noinput`
   - `python manage.py migrate --noinput`
   - `gunicorn treehole.wsgi:application`
6. Once live, visit the Render dashboard → **Shell** if you need to create a Django superuser.

### Option B: Manual Web Service (fallback)

1. **Local git commit & push**
   ```bash
   git add .
   git commit -m "Initial Django project scaffolding"
   git push origin main
   ```

2. **Render Web Service Setup**
   - Click **New > Web Service**.
   - Connect your GitHub account and choose the `Mgmt-of-Software---Glyz-Team` repo.
   - Build command: `pip install -r requirements.txt`
   - (Optional) Pre-deploy command: `python manage.py collectstatic --noinput && python manage.py migrate --noinput`
   - Start command: `gunicorn treehole.wsgi:application`
   - Environment: `Python 3` (Render auto-detects Django).
   - Add environment variables (`DJANGO_SECRET_KEY`, `DATABASE_URL`, `DJANGO_ALLOWED_HOSTS`, `DB_SSL_REQUIRE=True`).
   - If you skip the pre-deploy command, open the Render shell after each deploy and run `python manage.py migrate`.

3. **Static files**
   - WhiteNoise is preconfigured; no extra Render storage needed.

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

