# Tree Hole Yale

Tree Hole Yale is an anonymous, Yale-only campus forum inspired by SideChat. Students can speak freely, react to posts, and flag content for moderation while keeping their identity private.

## Tech Stack

- Django 5 + Python 3.14 (virtualenv already provisioned in `venv/`)
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

- Users register via `/accounts/signup/`. Only emails ending with `@yale.edu` (configurable via `ALLOWED_EMAIL_DOMAINS` in your `.env`) are accepted.
- Successful signups are automatically logged in and redirected to the home feed.
- The `accounts` app uses Django's built-in auth views (`/accounts/login/`, `/accounts/logout/`).

---

## 4. GitHub & Render Deployment Workflow

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
   - Start command: `gunicorn treehole.wsgi:application`
   - Environment: `Python 3` (Render auto-detects Django).
   - Add environment variables (`DJANGO_SECRET_KEY`, `DATABASE_URL`, `DJANGO_ALLOWED_HOSTS`, `DB_SSL_REQUIRE=True`).

3. **Static files**
   - WhiteNoise is preconfigured; no extra Render storage needed.

### Using render.yaml (optional IaC)

- Render can auto-provision both the web app and database from `render.yaml`.
- From the Render dashboard, choose **Blueprint** deployment, select your repo, and approve the plan. Environment variables marked `sync: false` need to be entered manually the first time.

---

## 5. Project Structure

```
Tree Hole Yale/
├── env.example
├── manage.py
├── forum/               # Django app with models, admin, views
├── treehole/            # Project settings, URLs, ASGI/WSGI
├── templates/           # Base templates (placeholder home page)
├── static/              # Static assets (add CSS/JS here)
├── media/               # User-uploaded media (optional)
├── requirements.txt
└── venv/                # Virtualenv (kept locally, not pushed)
```

---

## 6. Next Steps

- Finish the anonymous post flow (forms, views, templates).
- Add upvote/flag endpoints and UI.
- Integrate Yale-only authentication (email domain check or SSO).
- Write tests for posting, voting, and flagging.
- Prepare `render.yaml` for Infrastructure-as-Code deployment (outlined later).

## 7. Testing & QA

- Run `python manage.py test` regularly as you add features.
- Use `python manage.py runserver` locally and navigate to `http://127.0.0.1:8000/` to test the posting flow.
- For integration testing, seed sample tags via the Django admin and ensure filtering works.
- Before each Render deploy, run `python manage.py collectstatic` locally to verify assets build.

