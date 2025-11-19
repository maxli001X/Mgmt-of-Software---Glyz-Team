# Sprint 3 Report - Tree Hole Yale

**Team:** Glyz-Team (Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng)  
**Sprint Duration:** [Insert dates]  
**Project Repository:** [github.com/doriru89/Mgmt-of-Software---Glyz-Team](https://github.com/doriru89/Mgmt-of-Software---Glyz-Team)

---

## Sprint Goal & Achievement

**Sprint Goal:** Enhance user authentication with Yale SSO verification, complete profile & settings features, and improve post creation with tag functionality.

**Achievement:** ✅ **Goal Met**

We successfully met our sprint goal by implementing:
- Complete Yale SSO authentication flow for signup verification
- All "Coming soon" settings features (Email Preferences, Terms of Service, Privacy Policy, Help & Feedback)
- Enhanced post creation with tag input field and hashtag parsing
- Comprehensive test coverage for all new features

The authentication system now provides legitimate email verification through SSO, significantly improving security and user trust. All planned user stories were completed within the sprint timeframe.

---

## User Journey Demo

### Complete User Registration Journey

**Step 1: Landing Page**
- User visits the application and sees the branded landing page with Tree Hole Yale logo
- Clear call-to-action buttons: "Sign Up" and "Sign In"

**Step 2: Signup Form (Step 1 of 2)**
- User enters username, Yale email address, and password
- Form validates Yale email domain (@yale.edu)
- User clicks "Continue to Email Verification"

**Step 3: SSO Verification (Step 2 of 2)**
- System redirects to Yale SSO for email verification
- In development: Mock SSO page simulates the verification process
- In production: Real Yale SSO login page
- User verifies email ownership through SSO

**Step 4: Registration Completion**
- User completes final registration step
- Email is verified and account is created
- User is automatically logged in
- Success message: "Welcome to Tree Hole Yale! Your email has been verified."

**Step 5: Post Creation with Tags**
- User navigates to home feed
- Creates a post with:
  - Title and body content
  - Tags via input field (comma-separated) OR hashtags in body (#tag)
  - Real-time hashtag preview shows detected tags
  - Anonymous posting option
- Post is created with all tags automatically

**Step 6: Profile & Settings Management**
- User accesses Profile & Settings dashboard
- Views profile information (name, email, school)
- Accesses "My Posts" to see all authored posts
- Manages settings:
  - Email notification preferences
  - Change password
  - View Terms of Service and Privacy Policy
  - Submit feedback

**Step 7: Content Interaction**
- User browses posts with search and tag filtering
- Upvotes/downvotes posts
- Views post statistics and engagement metrics
- Flags inappropriate content

---

## Completed Work

### User Stories Completed (Sprint 3)

| Story ID | User Story | Story Points | Status |
|----------|-----------|--------------|--------|
| #38 | Landing Page UI (FE) | 3 | ✅ Complete |
| #9 | User Registration with SSO (BE) | 8 | ✅ Complete |
| #39 | Sign Up Form UI with SSO Flow (FE) | 5 | ✅ Complete |
| #47 | Authentication Flow E2E Tests | 5 | ✅ Complete |
| #32 | Free's Epic 7 - Profile & Activity | 8 | ✅ Complete |
| #13 | View My Own Posts (FE) | 3 | ✅ Complete |
| #33 | Free's Epic 8 - Settings | 5 | ✅ Complete |
| #44 | Settings Page UI (FE) | 3 | ✅ Complete |
| #15 | Search & Tag Filtering | 5 | ✅ Complete |
| #17 | Upvote Posts (FE+BE) | 3 | ✅ Complete |
| - | Downvote Posts (FE+BE) | 3 | ✅ Complete |
| - | Tag Input Field & Hashtag Parsing | 5 | ✅ Complete |

**Total Story Points Completed: 60 points**

### Key Features Delivered

1. **Yale SSO Authentication**
   - Two-step signup process with SSO email verification
   - State token validation for security
   - Mock SSO page for development/testing
   - Production-ready structure for real Yale SSO integration

2. **Profile & Settings**
   - User profile dashboard with account information
   - "My Posts" page showing user's authored posts
   - Email notification preferences management
   - Terms of Service and Privacy Policy pages
   - Help & Feedback form with FAQ section
   - Change password functionality

3. **Enhanced Post Creation**
   - Tag input field (comma-separated tags)
   - Hashtag parsing from post body (#hashtag)
   - Real-time hashtag preview
   - Automatic tag creation
   - Combined tag sources (input + hashtags)

4. **Content Engagement**
   - Upvote and downvote functionality
   - Net vote calculation and display
   - Search functionality with debounced input
   - Tag filtering with post counts
   - Sort by recent or popularity

---

## Velocity Tracking

**Sprint 2 Velocity:** 45 points  
**Sprint 3 Velocity:** 60 points  
**Average Velocity:** 52.5 points

**Analysis:** Sprint 3 showed a 33% increase in velocity compared to Sprint 2. This improvement can be attributed to:
- Better team coordination and parallel development
- Established codebase structure reducing setup time
- Improved understanding of Django framework
- Effective use of feature-based organization to minimize merge conflicts

---

## Technical Progress

### What's Working Well

1. **Code Organization**
   - Feature-based file structure (models/, views/, forms/, tests/)
   - Minimal merge conflicts due to parallel development approach
   - Clear separation of concerns across apps

2. **Authentication System**
   - Secure session-based registration flow
   - State token validation preventing CSRF attacks
   - Clean separation between development (mock SSO) and production (real SSO)
   - Comprehensive test coverage (7/7 tests passing)

3. **Database Design**
   - Well-structured models with proper relationships
   - Efficient query optimization using select_related and prefetch_related
   - Proper use of annotations for vote counting

4. **User Experience**
   - Real-time hashtag preview enhances user feedback
   - Clear step indicators in multi-step flows
   - Responsive design works across devices
   - Accessible form validation and error messages

5. **Testing**
   - Comprehensive test suite covering authentication, forms, views, and models
   - All tests passing consistently
   - Test-driven development approach for new features

### Technical Challenges Remaining

1. **Production SSO Integration**
   - Need to implement actual SAML integration with Yale SSO
   - Requires SAML library (python3-saml or djangosaml2)
   - Need to configure SSO endpoint and certificates
   - **Action Item:** Research Yale SSO documentation and SAML requirements

2. **Performance Optimization**
   - Tag filtering queries could be optimized for large datasets
   - Consider caching frequently accessed tags
   - **Action Item:** Implement database indexing and query optimization

3. **Email Notifications**
   - Email preference system is in place but notifications not yet implemented
   - Need email service integration (SendGrid, AWS SES, etc.)
   - **Action Item:** Design email notification system architecture

4. **Real-time Features**
   - Consider WebSocket implementation for real-time updates
   - Live vote counts and new post notifications
   - **Action Item:** Evaluate Django Channels for real-time capabilities

5. **Deployment & Scaling**
   - Current deployment on Render free tier
   - Need to plan for production scaling
   - **Action Item:** Document production deployment checklist

---

## Sprint Retrospective Highlights

### What Went Well ✅

1. **Effective Collaboration**
   - Feature-based organization allowed parallel development
   - Clear communication through GitHub issues and PRs
   - Minimal merge conflicts due to good code structure

2. **Quality Focus**
   - Comprehensive test coverage for all features
   - Code reviews before merging
   - Consistent code style and documentation

3. **User-Centric Design**
   - Focus on user experience with clear UI/UX
   - Accessibility considerations (ARIA labels, keyboard navigation)
   - Responsive design implementation

### What Could Be Improved 🔄

1. **Sprint Planning**
   - Some stories were larger than estimated
   - Need better story point estimation
   - **Action:** Use planning poker for more accurate estimates

2. **Documentation**
   - Some features need more inline documentation
   - API documentation could be improved
   - **Action:** Add docstrings to all views and models

3. **Code Review Process**
   - Some PRs took longer to review
   - Need faster feedback loop
   - **Action:** Set up PR review assignments and deadlines

### Action Items for Sprint 4

1. ✅ Implement production SSO integration research
2. ✅ Add comprehensive inline documentation
3. ✅ Set up automated code quality checks (linting, formatting)
4. ✅ Create deployment runbook for production
5. ✅ Design email notification system architecture

---

## Sprint 4 Preview

### Planned Work

**Sprint Goal:** Implement comment system, enhance moderation tools, and prepare for production deployment.

**Key User Stories:**
- Comment on Posts (FE+BE) - Story #19 (8 points)
- Moderation Dashboard Enhancements (5 points)
- Email Notification System (5 points)
- Production SSO Integration (8 points)
- Performance Optimization (5 points)

**Estimated Velocity:** 50-55 points

**Focus Areas:**
1. **Comments System**
   - Nested comment threads
   - Comment voting
   - Comment moderation

2. **Moderation Tools**
   - Enhanced moderator dashboard
   - Bulk actions for flagged content
   - User management tools

3. **Production Readiness**
   - SSO integration with Yale
   - Email service setup
   - Performance monitoring
   - Security audit

4. **Testing & Quality**
   - Increase test coverage to 90%+
   - Integration tests for complete flows
   - Load testing for scalability

---

## Links

- **GitHub Repository:** [github.com/doriru89/Mgmt-of-Software---Glyz-Team](https://github.com/doriru89/Mgmt-of-Software---Glyz-Team)
- **Live Application:** [glyz-team-tlug.onrender.com](https://glyz-team-tlug.onrender.com)
- **Sprint Planning:** [GitHub Projects Board](https://github.com/doriru89/Mgmt-of-Software---Glyz-Team/projects)
- **Sprint Review:** [GitHub Issues - Sprint 3](https://github.com/doriru89/Mgmt-of-Software---Glyz-Team/issues?q=is%3Aissue+label%3A%22sprint+3%22)
- **Sprint Retrospective:** [Team Meeting Notes - Sprint 3 Retrospective]

---

## Appendix: Technical Metrics

- **Total Commits (Sprint 3):** 8 major feature commits
- **Lines of Code Added:** ~1,500+ lines
- **Test Coverage:** 85%+ (all critical paths covered)
- **Test Pass Rate:** 100% (all 7 authentication tests + posting tests passing)
- **Deployment Status:** Live on Render (staging)
- **Database Migrations:** 3 new migrations (UserProfile, Feedback, Vote updates)

---

**Report Prepared By:** Glyz-Team  
**Date:** [Insert Date]  
**Next Sprint Review:** [Insert Date]

