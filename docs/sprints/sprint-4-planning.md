# Sprint 4 Planning

**Sprint Goal:** Deploy to production, implement A/B endpoint with analytics, and complete remaining MVP features.
**Duration:** [Current Date] - [Final Submission Date]

## Sprint Goal
By the end of Sprint 4, we will have a production-ready application deployed to a public URL, with a working A/B test endpoint tracked by analytics, and all core MVP features polished and bug-free.

## Selected User Stories

### 1. Production Deployment (Critical)
- **Story:** As a user, I want to access the application on a public URL so that I can use it from anywhere.
- **Tasks:**
    - Configure production environment variables.
    - Deploy to Render/Fly.io.
    - Verify database connection and static files.
- **Points:** 5

### 2. A/B Test Endpoint (Critical)
- **Story:** As a professor/grader, I want to access `/{hash}` to see the team roster and A/B test button.
- **Tasks:**
    - Implement route `/972b69d`.
    - Create view with team nicknames.
    - Implement "kudos" vs "thanks" button logic.
- **Points:** 5

### 3. Analytics Tracking (Critical)
- **Story:** As a developer, I want to track visits and clicks on the A/B test page to analyze user preference.
- **Tasks:**
    - Implement `ABTestLog` model.
    - Track page views.
    - Track button clicks.
- **Points:** 5

### 4. Documentation & Quality
- **Story:** As a maintainer, I want clear documentation and clean code so that the project is easy to hand off.
- **Tasks:**
    - Update README.
    - Create Sprint Review and Retrospective docs.
    - Ensure all tests pass.
- **Points:** 3

## Team Assignments
- **All Members:** Production deployment verification, final QA.
- **[Your Name/Role]:** A/B Test Endpoint, Analytics, Documentation.

## Risks & Mitigation
- **Deployment Issues:** Risk of configuration errors on production. Mitigation: Deploy early and test thoroughly.
- **Analytics Data:** Risk of not capturing data. Mitigation: Test locally and verify logs in admin panel.
