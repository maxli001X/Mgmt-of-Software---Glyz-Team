# Render Deployment Checklist

Use this checklist to ensure a smooth deployment to Render.

## Pre-Deployment Checklist

### ✅ Code Quality
- [ ] All changes committed to git
- [ ] Code tested locally
- [ ] No hardcoded secrets or API keys
- [ ] `.env` file not committed (should be in `.gitignore`)

### ✅ Configuration Files
- [ ] `render.yaml` - Blueprint configuration exists
- [ ] `runtime.txt` - Python version specified (3.12.0)
- [ ] `requirements.txt` - All dependencies listed
- [ ] `Procfile` - Web process defined
- [ ] `.renderignore` - Unnecessary files excluded
- [ ] `build.sh` - Build script (if using custom build)

### ✅ Django Settings
- [ ] `ALLOWED_HOSTS` configured in `settings.py` to read from environment
- [ ] `CSRF_TRUSTED_ORIGINS` configured properly
- [ ] `SECRET_KEY` reads from environment variable
- [ ] `DEBUG` reads from environment (False in production)
- [ ] `DATABASES` configured to use `DATABASE_URL`
- [ ] `STATIC_ROOT` and `STATICFILES_STORAGE` configured
- [ ] WhiteNoise middleware installed and configured

### ✅ Dependencies
- [ ] `gunicorn` in `requirements.txt`
- [ ] `psycopg2-binary` in `requirements.txt`
- [ ] `dj-database-url` in `requirements.txt`
- [ ] `python-decouple` in `requirements.txt`
- [ ] `whitenoise` in `requirements.txt`

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy via Render Dashboard
- [ ] Go to [Render Dashboard](https://dashboard.render.com/)
- [ ] Click "New" → "Blueprint"
- [ ] Connect GitHub repository
- [ ] Select repository: `Mgmt-of-Software---Glyz-Team`
- [ ] Review Blueprint (should show web service + database)
- [ ] Click "Apply"

### 3. Monitor Deployment
- [ ] Watch build logs for errors
- [ ] Verify migrations run successfully
- [ ] Verify static files collected
- [ ] Check application starts without errors

### 4. Post-Deployment Verification
- [ ] Visit the deployed URL: `https://glyz-team.onrender.com`
- [ ] Test homepage loads
- [ ] Test login/signup pages
- [ ] Create superuser via Render Shell
- [ ] Access admin panel: `/admin/`
- [ ] Verify database connection works
- [ ] Test posting functionality
- [ ] Check static files load (CSS, images)

## Post-Deployment Tasks

### Create Superuser
```bash
# In Render Dashboard → Your Service → Shell
python manage.py createsuperuser
```

### Verify Environment Variables
Check these are set in Render Dashboard:
- [ ] `DJANGO_SECRET_KEY` (should be auto-generated)
- [ ] `DJANGO_ALLOWED_HOSTS`
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS`
- [ ] `DJANGO_DEBUG=False`
- [ ] `DATABASE_URL` (linked from database)
- [ ] `DB_SSL_REQUIRE=True`
- [ ] `ALLOWED_EMAIL_DOMAINS=yale.edu`

### Security Verification
- [ ] HTTPS enabled (should be automatic)
- [ ] Secure cookies enabled
- [ ] HSTS headers present
- [ ] Debug mode disabled (`DEBUG=False`)
- [ ] Admin panel accessible only to superusers
- [ ] Email validation working (Yale.edu only)

## Troubleshooting Common Issues

### Build Fails
- [ ] Check Python version in `runtime.txt` matches Render support
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Review build logs in Render Dashboard

### Database Connection Errors
- [ ] Verify `DATABASE_URL` environment variable is set
- [ ] Ensure database is in same region as web service
- [ ] Check `DB_SSL_REQUIRE=True` for Render PostgreSQL

### Static Files Not Loading
- [ ] Verify `collectstatic` ran in pre-deploy command
- [ ] Check WhiteNoise is in `INSTALLED_APPS` middleware
- [ ] Ensure `STATIC_ROOT` points to correct directory

### Application Won't Start
- [ ] Check Gunicorn start command is correct
- [ ] Verify `WSGI_APPLICATION` setting in Django
- [ ] Review application logs for Python errors
- [ ] Ensure migrations completed successfully

### 502 Bad Gateway
- [ ] Check if application is running (view logs)
- [ ] Verify health check endpoint (`/`) returns 200
- [ ] Ensure Gunicorn workers are starting
- [ ] Check for migration errors

## Monitoring After Deployment

### Daily Checks (First Week)
- [ ] Review application logs
- [ ] Check error rates
- [ ] Monitor response times
- [ ] Verify database connections

### Weekly Checks
- [ ] Review security headers
- [ ] Check for dependency updates
- [ ] Monitor disk usage (database)
- [ ] Review user feedback

## Optional Enhancements

### Custom Domain
- [ ] Purchase domain
- [ ] Add to Render service
- [ ] Update DNS records
- [ ] Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- [ ] Verify SSL certificate

### Email Configuration
- [ ] Choose email service (SendGrid, Mailgun, etc.)
- [ ] Configure `EMAIL_BACKEND` in settings
- [ ] Add API keys to environment variables
- [ ] Test email sending

### Error Monitoring
- [ ] Sign up for Sentry or similar
- [ ] Add Sentry SDK to requirements
- [ ] Configure Sentry in Django settings
- [ ] Test error reporting

### Performance
- [ ] Upgrade from free tier if needed
- [ ] Enable database connection pooling
- [ ] Configure CDN for static files
- [ ] Set up caching (Redis)

## Useful Commands

```bash
# View service logs
render logs --service glyz-team

# Open shell
render shell --service glyz-team

# Trigger manual deploy
render deploy --service glyz-team

# List all services
render services list

# View service details
render services get glyz-team
```

## Resources

- 📘 [Full Deployment Guide](./DEPLOYMENT.md)
- 📖 [Render Documentation](https://render.com/docs)
- 🐍 [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- 🔒 [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)

## Support

If you encounter issues:
1. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting
2. Review Render documentation
3. Check Django logs in Render Dashboard
4. Visit [Render Community](https://community.render.com)

---

**Last Updated**: Ready for Render Blueprint deployment with Python 3.12 and Django 5.2.8

