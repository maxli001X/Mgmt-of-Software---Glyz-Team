# Production Management

Quick reference for managing Tree Hole Yale in production.

**Live**: `https://glyz-team.onrender.com`

---

## Quick Access

- **Render Dashboard**: https://dashboard.render.com
- **Service**: `glyz-team` (web)
- **Database**: `glyz-team-db` (PostgreSQL)
- **Admin Panel**: https://glyz-team.onrender.com/admin/

---

## Daily Tasks

### Create Superuser

Open Shell in Render Dashboard:
```bash
python manage.py createsuperuser
```

Use @yale.edu email. Then access: https://glyz-team.onrender.com/admin/

### View Logs

Render Dashboard → Your Service → Logs tab

Watch for:
- 500 errors → Check application logs
- Migration errors → Run migrations (see below)
- CSS missing → Run collectstatic (see below)

### Run Management Commands

Open Shell in Render Dashboard:

```bash
# Migrations
python manage.py migrate
python manage.py showmigrations

# Static files (if CSS breaks)
python manage.py collectstatic --noinput

# Django shell
python manage.py shell

# Check system
python manage.py check
```

### Deploy Updates

```bash
# Local: commit and push
git add .
git commit -m "Your changes"
git push origin main

# Render auto-deploys (watch logs)
```

**Manual deploy**: Render Dashboard → Service → "Manual Deploy"

### Update Environment Variables

Render Dashboard → Service → Environment → Add/Edit

Common variables:
- `DJANGO_SECRET_KEY` (already set)
- `DATABASE_URL` (already linked)
- `ALLOWED_EMAIL_DOMAINS=yale.edu`

Save triggers automatic redeploy.

---

## Database

### Backup
```bash
# Manual backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

### Connect
```bash
# Get DATABASE_URL from Render Dashboard
psql <your-database-url>

# Or in Django shell
python manage.py dbshell
```

---

## Quick Fixes

### Site Down (502)
```bash
# In Render Shell
python manage.py migrate --noinput
python manage.py check
```

Check logs for Python errors.

### CSS Not Loading
```bash
# In Render Shell
python manage.py collectstatic --noinput
```

Hard refresh browser: Ctrl+Shift+R

### Database Connection Error
1. Render Dashboard → Database → Verify running
2. Check `DATABASE_URL` in environment
3. Test: `psql $DATABASE_URL -c "SELECT version();"`

### CSRF Error on Forms
Update in Render Dashboard → Environment:
```
DJANGO_CSRF_TRUSTED_ORIGINS=https://glyz-team.onrender.com
```

### Slow First Load (30-60s)
Free tier spins down after 15 min. Upgrade to Starter ($7/mo) for always-on.

---

## Update Dependencies

```bash
# Edit requirements.txt locally
pip install new-package
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

---

## Database Migrations

```bash
# Local: create migration
python manage.py makemigrations

# Commit migration files
git add */migrations/*.py
git commit -m "Add migration for X"
git push origin main

# Render runs migrations automatically
```

---

## Commands Reference

```bash
# Via Render CLI
render logs --service glyz-team
render shell --service glyz-team

# In Render Shell
python manage.py dbshell
python manage.py shell
python manage.py check --deploy
```

---

## Resources

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com

---

**For team collaboration, see [CONTRIBUTING.md](./CONTRIBUTING.md)**
