# Tree Hole Yale
### An Anonymous Campus Forum for the Yale Community

**Live Demo**: https://glyz-team-tlug.onrender.com

---

## Problem We're Solving

Students need a safe, anonymous space to share thoughts, ask questions, and discuss campus life without fear of judgment or social consequences.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 5.2 (Python 3.14) |
| **Database** | PostgreSQL (production) / SQLite (dev) |
| **AI/ML** | OpenAI Moderation API + scikit-learn TF-IDF |
| **Frontend** | Vanilla JS with AJAX, CSS3 |
| **Deployment** | Render.com + Gunicorn + WhiteNoise |
| **Security** | HTTPS, CSRF, HSTS, HttpOnly cookies |

---

## Core Features

### 1. Anonymous Posting System
- Post anonymously OR with profile identity
- Toggle per-post choice
- Soft delete preserves thread structure

### 2. Nested Comment Threads
- Infinite reply depth
- AJAX-powered real-time submission
- Upvote/downvote on comments

### 3. Smart Voting System
- Upvote/Downvote with toggle behavior
- Optimistic UI updates (instant feedback)
- Race condition handling

### 4. Tag-Based Discovery
- Auto-hashtag detection from post body (`#academics`)
- Manual tag input
- Filter posts by tag
- Tag post counts

---

## AI-Powered Features

### Content Moderation (OpenAI API)
- Real-time screening for hate speech, harassment, self-harm, violence
- Severity scoring (0-1 scale)
- Auto-flag for human review
- **Crisis detection** → Shows mental health resources

### Smart Tag Suggestions (scikit-learn)
- TF-IDF vectorization trained on existing posts
- 100% local processing (no API cost)
- Cosine similarity matching
- Suggests 4 relevant tags as you type

---

## Security Features

| Feature | Implementation |
|---------|----------------|
| **Yale-only Access** | Email domain validation (`@yale.edu`) |
| **Session Security** | HttpOnly, Secure, SameSite cookies |
| **CSRF Protection** | Token on all forms |
| **HSTS** | Strict-Transport-Security headers |
| **Content Moderation** | AI + human review workflow |

---

## Analytics & Statistics

### User Dashboard
- Personal stats: posts, votes received, tags used
- Activity timeline (first/last activity)

### Platform Analytics (Admin)
- DAU / WAU / MAU metrics
- Posts per day trend (7-day chart)
- Top 10 most popular tags
- Total users, posts, votes, flags

### A/B Testing
- Built-in variant tracking
- Click-through rate measurement
- Session-based assignment

---

## Moderation Dashboard (Staff Only)

- **Flagged Content Queue** sorted by AI severity score
- One-click actions: Unflag, Hide, Delete
- Soft delete preserves discussion context
- Separate handling for posts vs. comments
- Orphan tag cleanup on deletion

---

## Frontend Highlights

- **Responsive Design** - Mobile-first CSS
- **AJAX Everywhere** - No page reloads for votes, comments, flags
- **Keyboard Navigation** - Full accessibility support
- **Search Autocomplete** - Tags + recent posts suggestions
- **Infinite Scroll Ready** - Pagination with 12 posts/page
- **Optimistic UI** - Instant visual feedback before server confirms

---

## Trending Algorithm

```
score = (recent_votes × 2 + recent_comments) / (age_hours + 2)
```

- Database-native calculation (PostgreSQL/SQLite)
- 24-hour activity window
- Balances popularity vs. recency

---

## Architecture

```
Tree Hole Yale/
├── posting/          # Core forum (posts, comments, votes, tags)
├── auth_landing/     # Login, signup, Yale email validation
├── profile_settings/ # User profiles, preferences, feedback
├── moderation_ranking/ # Staff moderation tools
├── analytics/        # A/B testing, metrics
└── templates/        # 22 HTML templates
```

**Feature-based file organization** to minimize merge conflicts in team development.

---

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /posts/<id>/upvote/` | Vote on post |
| `POST /posts/<id>/comments/add/` | Add comment |
| `POST /api/suggest-tags/` | AI tag suggestions |
| `GET /api/search-suggestions/` | Search autocomplete |
| `GET /stats/` | Platform analytics |
| `POST /moderation/posts/<id>/hide/` | Hide flagged post |

---

## What We Learned

1. **Django ORM Optimization** - `select_related`, `prefetch_related` for N+1 prevention
2. **AI API Integration** - Graceful degradation when API unavailable
3. **Real-time UI** - AJAX patterns without frontend frameworks
4. **Security Best Practices** - CSRF, XSS prevention, domain validation
5. **Production Deployment** - Environment config, static files, PostgreSQL

---

## Key Differentiators

| Feature | Why It Matters |
|---------|----------------|
| **AI Moderation** | Scales safety without manual review of every post |
| **Crisis Detection** | Shows mental health resources when needed |
| **Anonymous + Identity** | Users choose per-post, not all-or-nothing |
| **Yale Email Lock** | Verified community, no outsider spam |
| **Nested Threads** | Reddit-style discussions, not flat comments |

---

## Future Roadmap

- Push notifications
- Direct messaging
- Course-specific communities
- Integration with Yale SSO (CAS)
- Mobile app (React Native)

---

## Thank You!

**Questions?**

**Try it**: https://glyz-team-tlug.onrender.com
