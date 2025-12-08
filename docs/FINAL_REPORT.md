# Tree Hole Yale - Final Project Report

**Team:** Glyz-Team
**Members:** Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng
**Course:** Management of Software Development
**Date:** December 7, 2025

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Burndown & Velocity Analysis](#2-burndown--velocity-analysis)
3. [A/B Test Traffic Analysis](#3-ab-test-traffic-analysis)
4. [Project Retrospective](#4-project-retrospective)
5. [Technical Summary](#5-technical-summary)

---

## 1. Project Overview

### Problem Statement
Yale students lack an anonymous platform to discuss campus life, share experiences, and seek support without fear of social consequences. Traditional social media ties posts to identity, which inhibits honest discourse on sensitive topics.

### Solution
**Tree Hole Yale** is an anonymous campus forum exclusively for Yale students. The name comes from the Chinese concept of "tree hole" (树洞) - a place to whisper secrets safely.

### Live URLs
- **Production:** https://glyz-team-tlug.onrender.com
- **A/B Test Endpoint:** https://glyz-team-tlug.onrender.com/972b69d/
- **Admin Panel:** https://glyz-team-tlug.onrender.com/admin/

### Core Features Implemented
1. **Anonymous Posting** - Users can post with or without identity
2. **Nested Comments** - Infinite-depth threaded discussions
3. **Voting System** - Upvote/downvote with toggle behavior
4. **Tag System** - Manual tags and auto-hashtag detection
5. **AI Content Moderation** - OpenAI-powered safety detection with crisis resources
6. **Moderator Dashboard** - Flagged content queue with bulk actions
7. **User Profiles** - Statistics, settings, and feedback submission
8. **Search & Discovery** - Full-text search with trending algorithm
9. **A/B Testing** - Analytics endpoint with variant tracking

---

## 2. Burndown & Velocity Analysis

### Sprint Velocity Summary

| Sprint | Duration | Planned Points | Completed Points | Velocity |
|--------|----------|----------------|------------------|----------|
| Sprint 1 | Week 1-2 | N/A | N/A | (Setup) |
| Sprint 2 | Week 3-4 | 45 | 45 | 45 pts |
| Sprint 3 | Week 5-6 | 60 | 60 | 60 pts |
| Sprint 4 | Week 7-8 | 31 | 31 | 31 pts |
| **Total** | 8 weeks | **136** | **136** | **Avg: 45 pts** |

### Burndown Chart (All Sprints)

```
Story Points Remaining
│
80 ┤ Sprint 2
   │ ████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░
60 ┤                                              Sprint 3
   │                                              ████████████████████████████████████████████████████████████░░░░░░
40 ┤                                                                                                              Sprint 4
   │                                                                                                              ████████████████████████████████
20 ┤
   │
 0 ┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   │  W1    W2    W3    W4    W5    W6    W7    W8
   └────────────────────────────────────────────────
                        Time (Weeks)
```

### Velocity Trend Analysis

```
Velocity (Story Points per Sprint)
│
70 ┤
60 ┤              ████████
50 ┤    ████████  ████████
40 ┤    ████████  ████████           ████████
30 ┤    ████████  ████████           ████████
20 ┤    ████████  ████████           ████████
10 ┤    ████████  ████████           ████████
 0 ┼────────────────────────────────────────────
        Sprint 2   Sprint 3   Sprint 4
        (45 pts)   (60 pts)   (31 pts)
```

**Analysis:**
- **Sprint 2 (45 pts):** Foundation sprint - authentication, basic posting, database setup
- **Sprint 3 (60 pts):** Peak velocity - profile system, settings, tag functionality, voting
- **Sprint 4 (31 pts):** Deployment focus - A/B testing, production deployment, polish

The velocity decrease in Sprint 4 was intentional - we shifted focus from feature development to deployment, testing, and documentation. All committed work was completed each sprint (100% completion rate).

### Cumulative Flow

| Milestone | Cumulative Points | % Complete |
|-----------|-------------------|------------|
| End Sprint 2 | 45 | 33% |
| End Sprint 3 | 105 | 77% |
| End Sprint 4 | 136 | 100% |

---

## 3. A/B Test Traffic Analysis

### Endpoint Details
- **URL:** `/972b69d/` (computed from SHA1 of "Glyz-Team")
- **SHA1 Hash:** `972b69d648dd0dc7b8be509bb03cc015a2d8f73d`
- **Variant A:** Button displays "kudos"
- **Variant B:** Button displays "thanks"

### Implementation
Our A/B test uses session-based variant assignment:
- Each new session is randomly assigned Variant A or B
- Views and clicks are logged to `ABTestLog` database table
- Duplicate clicks from the same session are prevented
- Analytics tracked: timestamp, variant, event_type, session_key, IP, user_agent

### Traffic Data Analysis

To retrieve production analytics, run the following query:

```python
# Connect to production database and run:
from analytics.models import ABTestLog
from django.db.models import Count

# Get view counts per variant
views = ABTestLog.objects.filter(event_type='view').values('variant').annotate(count=Count('id'))

# Get click counts per variant
clicks = ABTestLog.objects.filter(event_type='click').values('variant').annotate(count=Count('id'))

# Calculate CTR for each variant
for v in ['A', 'B']:
    view_count = ABTestLog.objects.filter(event_type='view', variant=v).count()
    click_count = ABTestLog.objects.filter(event_type='click', variant=v).count()
    ctr = (click_count / view_count * 100) if view_count > 0 else 0
    print(f'Variant {v}: {view_count} views, {click_count} clicks, CTR: {ctr:.2f}%')
```

### Results

| Metric | Variant A ("kudos") | Variant B ("thanks") |
|--------|---------------------|----------------------|
| Total Views | [Query Production] | [Query Production] |
| Total Clicks | [Query Production] | [Query Production] |
| Click-Through Rate | [Calculate] | [Calculate] |

### Conclusion

**Preferred Variant:** [To be determined from production analytics]

Based on the click-through rate analysis, the bot traffic showed a preference for:
- **If CTR(A) > CTR(B):** Variant A ("kudos") is preferred
- **If CTR(B) > CTR(A):** Variant B ("thanks") is preferred

*Note: Run the analytics query on production database to determine the actual preferred variant.*

---

## 4. Project Retrospective

### What Went Well

1. **Feature-Based Code Organization**
   - Separate files per feature (`models/post.py`, `views/feed.py`, etc.)
   - Minimal merge conflicts despite parallel development
   - Clear module boundaries enabled independent work

2. **AI Content Moderation**
   - OpenAI Moderation API integration worked seamlessly
   - Crisis detection provides mental health resources automatically
   - Severity scoring helps moderators prioritize

3. **Test-Driven Development**
   - 119 automated tests covering all critical paths
   - Tests caught bugs before deployment
   - High confidence in refactoring

4. **Deployment Pipeline**
   - Render auto-deployment from GitHub main branch
   - Environment variables properly configured
   - PostgreSQL in production, SQLite for local development

5. **Agile Process**
   - Consistent sprint velocity tracking
   - Clear user stories with acceptance criteria
   - Regular retrospectives drove improvements

### Challenges Faced

1. **N+1 Query Problems**
   - Initial implementation had performance issues
   - Template calls like `post.get_net_votes` triggered extra queries
   - **Solution:** Used Django annotations and pre-computed values

2. **Open Redirect Vulnerability**
   - `_safe_redirect()` function had security flaw
   - Protocol-relative URLs could bypass host check
   - **Solution:** Added scheme validation in final security audit

3. **Temporary Code in Production**
   - Admin setup endpoint was left exposed
   - **Solution:** Removed before final submission

4. **A/B Test Implementation**
   - Initially considered Google Analytics, too complex
   - **Solution:** Self-rolled simple database tracking

5. **Time Management**
   - Sprint 4 required rushing documentation
   - Deployment took longer than expected due to environment variable configuration

### Key Learnings

1. **Deploy Early, Deploy Often**
   - Should have deployed to production in Sprint 2
   - Caught environment-specific issues late

2. **Security Audits Are Essential**
   - Final code review found 4 critical issues
   - Automated linting doesn't catch logic vulnerabilities

3. **Simple Solutions Win**
   - Self-rolled A/B analytics was faster than integrating GA
   - Avoid over-engineering for MVP

4. **Django's ORM is Powerful but Tricky**
   - Easy to write inefficient queries
   - `select_related` and `prefetch_related` are essential

5. **Documentation Pays Off**
   - CLAUDE.md helped AI assistants understand the codebase
   - Sprint documentation made retrospectives meaningful

### What We Would Do Differently

1. **Start with Production Deployment**
   - Set up CI/CD pipeline in Sprint 1
   - Deploy skeleton app immediately

2. **Implement Performance Monitoring**
   - Add Django Debug Toolbar from the start
   - Track query counts in development

3. **More Integration Tests**
   - Unit tests passed but integration issues appeared
   - Should test complete user flows

4. **Smaller User Stories**
   - Some 8-point stories should have been split
   - Smaller stories = more predictable velocity

5. **Earlier Security Review**
   - Security audit in Sprint 3 instead of Sprint 4
   - Use tools like `bandit` for Python security scanning

---

## 5. Technical Summary

### Technology Stack
| Layer | Technology |
|-------|------------|
| Backend | Django 5.2, Python 3.12 |
| Database | PostgreSQL (prod), SQLite (dev) |
| Frontend | Vanilla JS, HTML5, CSS3 |
| AI/ML | OpenAI Moderation API, scikit-learn |
| Deployment | Render.com, Gunicorn, WhiteNoise |

### Database Schema
- **5 Django apps:** posting, auth_landing, moderation_ranking, profile_settings, analytics
- **8 database models:** Post, Tag, Vote, Comment, CommentVote, UserProfile, Feedback, ABTestLog
- **Proper relationships:** ForeignKey, ManyToMany, OneToOne
- **Indexes:** Added for performance on frequently queried fields

### Test Coverage
- **119 automated tests**
- **Test types:** Unit, integration, form validation, view tests
- **All tests passing**

### 12-Factor Compliance
| Factor | Implementation |
|--------|----------------|
| Codebase | Git + GitHub |
| Dependencies | requirements.txt |
| Config | Environment variables via python-decouple |
| Backing Services | PostgreSQL as attached resource |
| Build/Release/Run | Render deployment pipeline |
| Processes | Stateless Gunicorn workers |
| Port Binding | Dynamic via $PORT |
| Concurrency | 2 Gunicorn workers |
| Disposability | Fast startup, graceful shutdown |
| Dev/Prod Parity | Same Django app, different configs |
| Logs | stdout via Gunicorn |
| Admin Processes | Django management commands |

### Security Measures
- CSRF protection on all forms
- HTTPS enforced in production
- Password hashing (Django default)
- Yale email domain validation
- Session-based authentication
- Open redirect vulnerability fixed
- No secrets in codebase

---

## Appendix: Links & Resources

- **GitHub Repository:** https://github.com/doriru89/Mgmt-of-Software---Glyz-Team
- **Production URL:** https://glyz-team-tlug.onrender.com
- **A/B Endpoint:** https://glyz-team-tlug.onrender.com/972b69d/
- **Sprint Documentation:** `/docs/sprints/`
- **README:** `/README.md`
- **Deployment Guide:** `/DEPLOYMENT.md`

---

**Report Prepared By:** Glyz-Team
**Date:** December 7, 2025
