# Tree Hole Yale

**Anonymous Yale-only campus forum** - Students speak freely, react to posts, and flag content for moderation.

🔗 **Live**: `https://glyz-team.onrender.com`  
🔗 **Repo**: [github.com/doriru89/Mgmt-of-Software---Glyz-Team](https://github.com/doriru89/Mgmt-of-Software---Glyz-Team)

---

## Quick Start (Local Development)

```bash
source venv/bin/activate
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Where to Find What

📖 **Adding features or collaborating?** → [CONTRIBUTING.md](./CONTRIBUTING.md)  
🚀 **Managing production or troubleshooting?** → [DEPLOYMENT.md](./DEPLOYMENT.md)  
📊 **Issue status?** → See table below

---

## Project Structure Explained

```
├── treehole/              # PROJECT CONFIGURATION (Django settings & routing)
│   ├── settings.py        # Database, apps, security configuration
│   └── urls.py            # Master URL routing
│
├── templates/             # HTML PAGES (what users see in browser)
│   ├── base.html          # Master layout
│   ├── auth_landing/      # Login/signup pages
│   └── posting/           # Forum pages
│
├── auth_landing/          # AUTHENTICATION APP (login, signup logic)
├── posting/               # FORUM APP (posts, tags, voting logic)
│   ├── models/            # post.py, tag.py, vote.py
│   ├── views/             # feed.py, post_actions.py
│   ├── forms/             # post_form.py
│   └── tests/             # test_*.py
├── moderation_ranking/    # MODERATION APP (moderator tools)
├── profile_settings/      # PROFILE APP (user profiles)
│
├── static/                # CSS, JAVASCRIPT, IMAGES
└── media/                 # USER UPLOADS (future)
```

**Key Concepts:**
- `treehole/` = Configuration brain (how the project runs)
- `templates/` = HTML pages (what users see)
- App folders (`posting/`, etc.) = Business logic (how features work)

**Details in [CONTRIBUTING.md](./CONTRIBUTING.md)**

---

## Quick Commands

```bash
# Run tests
python manage.py test
python manage.py test posting  # Specific app

# Database
python manage.py makemigrations  # After model changes
python manage.py migrate
python manage.py createsuperuser

# Django shell (create test data)
python manage.py shell

# Check for issues
python manage.py check
```

---

## Environment Variables

Create `.env` from `env.example`:

```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_EMAIL_DOMAINS=yale.edu
```

---

## Tech Stack

Django 5.2.8 + Python 3.12 | PostgreSQL | WhiteNoise | Deployed on Render

---

## Issue Status

| Issue | Feature | Status |
|-------|---------|--------|
| #39-40 | Auth (signup, login) | ✅ Complete |
| #41-42 | Tags, post composer | ✅ Complete |
| #43-45 | Profile & settings | 🚧 In Progress |
| #46 | Design system | ✅ Complete |
| #47-49 | Testing | ✅ Complete |
| #50 | Moderation | 🚧 In Progress |

---

## Team

**Glyz-Team**: Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng

---

## Resources

- **Django Docs**: https://docs.djangoproject.com
- **Render Dashboard**: https://dashboard.render.com
