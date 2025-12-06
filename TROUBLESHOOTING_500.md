# Troubleshooting 500 Server Error on Render

## Quick Steps to Diagnose

### 1. Check Render Logs (Most Important!)
Go to Render Dashboard → Your Service (`glyz-team`) → **Logs** tab

Look for:
- Python tracebacks (red errors)
- Import errors
- Database connection errors
- Missing environment variables
- Migration errors

### 2. Common Causes & Fixes

#### A. Missing Database Migrations
**Symptoms**: Database-related errors in logs

**Fix**:
```bash
# In Render Shell
python manage.py migrate --noinput
python manage.py showmigrations
```

#### B. Missing Environment Variables
**Symptoms**: `DJANGO_SECRET_KEY` errors, `DATABASE_URL` errors

**Check in Render Dashboard** → Service → Environment:
- ✅ `DJANGO_SECRET_KEY` (should be auto-generated)
- ✅ `DATABASE_URL` (should be linked from database)
- ✅ `DJANGO_ALLOWED_HOSTS=glyz-team-tlug.onrender.com,.onrender.com`
- ✅ `DJANGO_CSRF_TRUSTED_ORIGINS=https://glyz-team-tlug.onrender.com`
- ✅ `DJANGO_DEBUG=False`
- ✅ `ALLOWED_EMAIL_DOMAINS=yale.edu`

**Fix**: Add missing variables in Render Dashboard → Environment

#### C. Database Connection Issues
**Symptoms**: `psycopg2` errors, connection timeout

**Fix**:
1. Check database is running: Render Dashboard → Database → Status
2. Verify `DATABASE_URL` is correct
3. Test connection in Render Shell:
   ```bash
   python manage.py dbshell
   ```

#### D. Static Files Not Collected
**Symptoms**: CSS/JS not loading (but this wouldn't cause 500)

**Fix**:
```bash
# In Render Shell
python manage.py collectstatic --noinput
```

#### E. Import Errors
**Symptoms**: `ModuleNotFoundError`, `ImportError` in logs

**Check**:
- All packages in `requirements.txt` are installed
- Python version matches (should be 3.12.0 per render.yaml)

**Fix**: Check `requirements.txt` includes all dependencies

#### F. Template Errors
**Symptoms**: `TemplateDoesNotExist`, template syntax errors

**Fix**: Check template files exist and are properly formatted

### 3. Run Diagnostic Commands

In Render Shell (Render Dashboard → Service → Shell):

```bash
# Check Django configuration
python manage.py check --deploy

# Check database connection
python manage.py dbshell -c "SELECT version();"

# List all migrations
python manage.py showmigrations

# Check for unapplied migrations
python manage.py migrate --plan

# Test imports
python -c "import django; print(django.get_version())"
python -c "from treehole import settings; print('Settings loaded')"
```

### 4. Check Recent Changes

If this started after a recent deploy:
1. Check git commit history
2. Review recent code changes
3. Check if new migrations were added
4. Verify new dependencies were added to `requirements.txt`

### 5. Specific Issues to Check

#### AI Moderation (Should NOT cause 500)
The AI moderator handles missing `OPENAI_API_KEY` gracefully, so this shouldn't cause a 500 error.

#### Database Models
Check if all migrations are applied:
```bash
python manage.py showmigrations
```

Look for `[ ]` (unapplied) migrations and run:
```bash
python manage.py migrate
```

### 6. Emergency Fixes

If site is completely down:

1. **Check if service is running**: Render Dashboard → Service status
2. **Manual Deploy**: Render Dashboard → Service → "Manual Deploy"
3. **Rollback**: If recent deploy broke it, revert to previous commit
4. **Check Build Logs**: Render Dashboard → Service → Deploys → Latest → Build Logs

### 7. Get Detailed Error Information

The most important step is to **check the Render logs** to see the actual error message. The logs will show:
- The exact Python exception
- The file and line number where it occurred
- The full stack trace

**To access logs**:
1. Go to https://dashboard.render.com
2. Click on your service (`glyz-team`)
3. Click the **Logs** tab
4. Look for red error messages
5. Copy the full error traceback

### 8. Common Error Patterns

#### `OperationalError: no such table`
→ Run migrations: `python manage.py migrate`

#### `ImproperlyConfigured: SECRET_KEY`
→ Check `DJANGO_SECRET_KEY` environment variable

#### `DisallowedHost`
→ Check `DJANGO_ALLOWED_HOSTS` includes your domain

#### `ModuleNotFoundError: No module named 'X'`
→ Add missing package to `requirements.txt` and redeploy

#### `TemplateDoesNotExist`
→ Check template path and file exists

#### `Database connection failed`
→ Check database is running and `DATABASE_URL` is correct

---

## Next Steps

1. **Check Render Logs** (most important!)
2. **Run diagnostic commands** in Render Shell
3. **Check environment variables** in Render Dashboard
4. **Verify migrations** are applied
5. **Check recent code changes** if error started after deploy

Once you have the actual error from the logs, we can provide a specific fix!

