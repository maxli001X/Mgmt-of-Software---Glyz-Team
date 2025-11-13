# Forum Epic Story ↔ Code Mapping

This document maps the current Django codebase to the open forum epic stories tracked in GitHub issues. Use it as the source of truth for where each vertical slice lives in the repository.

| Issue | Story Scope | Primary Files |
|-------|-------------|---------------|
| #39 – Sign Up Form UI (FE) | Yale-only signup flow; form validation, template, success redirect | `auth_landing/forms.py`, `auth_landing/views.py`, `auth_landing/templates/auth_landing/signup.html`, `treehole/urls.py` |
| #40 – Sign In Form UI (FE) | Login/logout views and pages | `auth_landing/views.py`, `auth_landing/templates/auth_landing/login.html`, `auth_landing/templates/auth_landing/logout.html` |
| #41 – Tag Filtering Backend API (BE) | Filter feed by tag slug, expose tags for UI | `posting/views/feed.py` (`home` view), `posting/models/tag.py` (`Tag`), `posting/urls.py` |
| #42 – Post Composer UI (FE) | Anonymous post form with tag selection | `posting/forms/post_form.py`, `posting/templates/posting/home.html` (form section), `posting/views/feed.py` |
| #43 – Profile & My Posts Backend API (BE) | **Not yet implemented** – structured in `profile_settings/models/`, `profile_settings/views/profile.py` |
| #44 – Settings Page UI (FE) | **Not yet implemented** – structured in `profile_settings/forms/`, `templates/profile_settings/dashboard.html` |
| #45 – Settings Backend API (BE) | **Not yet implemented** – reserved for `profile_settings/forms/`, `profile_settings/views/profile.py` |
| #46 – Design System Components (FE) | Base layout, navigation, shared styling | `templates/base.html`, `static/css/styles.css` |
| #47 – Authentication Flow E2E Tests | Covered by signup/login/logout flows in `auth_landing` |
| #48 – Feed & Voting E2E Tests | Feed rendering, upvote + flag actions | `posting/views/feed.py`, `posting/views/post_actions.py`, `posting/tests/test_post_actions.py`, `posting/templates/posting/home.html`, `posting/urls.py`, `posting/models/vote.py` (`Vote`) |
| #49 – Post Creation E2E Tests | Posting pipeline (form submission, success messaging) | `posting/forms/post_form.py`, `posting/views/feed.py`, `posting/tests/test_forms.py` |
| #50 – Content Moderation E2E Tests | Flagging behaviour, admin tooling | `posting/views/post_actions.py` (`flag_post`), `posting/admin.py` (flag filters), `moderation_ranking/views/dashboard.py` |

> **Note:** Stories #43–#45 are represented by placeholder views/models/forms ready for implementation in the `profile_settings` app with feature-organized structure.

## Feature-Based Structure Benefits

The codebase now uses a feature-based organization that allows multiple developers to work on different stories without file conflicts:

- **Models** are split by domain (`tag.py`, `post.py`, `vote.py`) - add new models in separate files
- **Views** are split by feature (`feed.py`, `post_actions.py`) - add new views in separate files  
- **Forms** are split by purpose (`post_form.py`) - add new forms in separate files
- **Tests** are split by feature (`test_feed.py`, `test_forms.py`, `test_post_actions.py`) - add new tests in separate files

This structure minimizes merge conflicts and allows parallel development on different user stories.
