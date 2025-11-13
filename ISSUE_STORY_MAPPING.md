# Forum Epic Story ↔ Code Mapping

This document maps the current Django codebase to the open forum epic stories tracked in GitHub issues. Use it as the source of truth for where each vertical slice lives in the repository.

| Issue | Story Scope | Primary Files |
|-------|-------------|---------------|
| #39 – Sign Up Form UI (FE) | Yale-only signup flow; form validation, template, success redirect | `auth_landing/forms.py`, `auth_landing/views.py`, `auth_landing/templates/auth_landing/signup.html`, `treehole/urls.py` |
| #40 – Sign In Form UI (FE) | Login/logout views and pages | `auth_landing/views.py`, `auth_landing/templates/auth_landing/login.html`, `auth_landing/templates/auth_landing/logout.html` |
| #41 – Tag Filtering Backend API (BE) | Filter feed by tag slug, expose tags for UI | `posting/views.py` (`home` view), `posting/models.py` (`Tag`), `posting/urls.py` |
| #42 – Post Composer UI (FE) | Anonymous post form with tag selection | `posting/forms.py`, `posting/templates/posting/home.html` (form section), `posting/views.py` |
| #43 – Profile & My Posts Backend API (BE) | **Not yet implemented** – stub available in `profile_settings` app |
| #44 – Settings Page UI (FE) | **Not yet implemented** – stub available in `profile_settings` app |
| #45 – Settings Backend API (BE) | **Not yet implemented** – reserved for `profile_settings` app |
| #46 – Design System Components (FE) | Base layout, navigation, shared styling | `templates/base.html`, `static/css/styles.css` |
| #47 – Authentication Flow E2E Tests | Covered by signup/login/logout flows in `auth_landing` |
| #48 – Feed & Voting E2E Tests | Feed rendering, upvote + flag actions | `posting/views.py`, `posting/templates/posting/home.html`, `posting/urls.py`, `posting/models.py` (`Vote`) |
| #49 – Post Creation E2E Tests | Posting pipeline (form submission, success messaging) | `posting/forms.py`, `posting/views.py` |
| #50 – Content Moderation E2E Tests | Flagging behaviour, admin tooling | `posting/views.py` (`flag_post`), `posting/admin.py` (flag filters) |

> **Note:** Stories #43–#45 are represented by placeholder views/templates ready for implementation in the `profile_settings` app.




