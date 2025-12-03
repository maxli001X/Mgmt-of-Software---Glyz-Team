# Sprint 4 Report

**Team:** Glyz-Team
**Date:** [Current Date]

## Sprint Goal & Achievement
**Goal:** Deploy to production, implement A/B endpoint with analytics, complete MVP features, and finalize UI/UX polish.
**Achievement:** ✅ **Goal Met**

## Production Deployment
- **URL**: https://glyz-team-tlug.onrender.com
- **Status**: Stable. All core features are working.
- **Deployment Method**: Automated deployment via Render connected to GitHub `main` branch.

## A/B Test Endpoint
- **URL**: https://glyz-team-tlug.onrender.com/972b69d/
- **Functionality**:
    - Displays team roster: Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng.
    - **Variant A**: "kudos" button.
    - **Variant B**: "thanks" button.
    - **Analytics**: Tracks views and clicks in `ABTestLog` database table.
    - **Branding**: Applied "Tree Hole Yale" branding.
    - **Feedback**: Implemented inline success messages and button disabling to prevent spam.
    - **Duplicate Prevention**: Added server-side logic to reject duplicate clicks from the same session.

## Completed Work
### Core & Deployment
- **Production Deployment** (5 pts)
- **A/B Test Endpoint** (5 pts)
- **Analytics Tracking** (5 pts)
- **Documentation** (3 pts)

### Enhancements & Polish
- **UI/UX Improvements** (5 pts)
    - Branding updates
    - Inline feedback and spam prevention
- **Feature Enhancements** (5 pts)
    - **Auto-Collapse**: Implemented JavaScript logic to automatically truncate posts longer than 250 words with a "Read more" expansion.
    - **Robust Tags**: Added validation to `PostForm` to enforce tag length limits (2-50 characters).
- **Code Refinements** (3 pts)
    - **Security**: Removed `csrf_exempt` from analytics endpoints.
    - **Performance**: Added database indexes (`db_index=True`) to `ABTestLog`.

**Total Velocity:** 31 points

## Velocity Summary
- **Sprint 2**: 45 points
- **Sprint 3**: 60 points
- **Sprint 4**: 31 points (Deployment + Final Polish)
- **Average**: 45 points

## Readiness for Final Submission
- **Status**: Ready.
- **Complete**: Core MVP, Auth, Posting, Moderation, A/B Test, Deployment.
- **Polished Areas**: A/B Test page, Post display, Tag system.
- **Verification**: All new features are covered by automated tests.
- **Risks**: None identified.

## Retrospective Highlights
- **Learnings**: Importance of early deployment, simple analytics solutions, and continuous UI refinement.
- **Links**:
    - [Sprint Planning](./sprint-4-planning.md)
    - [Sprint Review](./sprint-4-review.md)
    - [Sprint Retrospective](./sprint-4-retrospective.md)
