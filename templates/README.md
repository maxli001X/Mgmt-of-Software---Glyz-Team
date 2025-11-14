# HTML Templates

This folder contains all HTML files that users see in their browsers.

## Structure
- `base.html` - Master layout (navbar, footer, shared elements)
- `auth_landing/` - Login, signup, logout pages
- `posting/` - Forum pages (feed, posts)
- `moderation_ranking/` - Moderator dashboard
- `profile_settings/` - User profile pages

## How it works
Django views render these templates to show pages to users.

Example: `/auth/login/` → loads `templates/auth_landing/login.html`

