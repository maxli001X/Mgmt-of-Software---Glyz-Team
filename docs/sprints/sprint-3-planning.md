# Sprint 3 Planning

**Sprint Goal:** Enhance user authentication with Yale SSO verification, complete profile & settings features, and improve post creation with enhanced tag functionality and voting system.
**Duration:** Week 5-6

## Sprint Goal
By the end of Sprint 3, users will have complete profile management, enhanced authentication with SSO verification, improved post creation with tag input and hashtag parsing, voting functionality, and search capabilities. This sprint focuses on user experience enhancements and feature completeness.

## Selected User Stories

### 1. Yale SSO Authentication (Critical)
- **Story:** As a user, I want to verify my Yale email through SSO so that my account is properly validated.
- **Tasks:**
    - Implement two-step signup process (form → SSO verification)
    - Create SSO verification view (mock for development, real for production)
    - State token validation for security
    - Handle SSO callback
    - Complete registration after SSO verification
- **Points:** 8
- **Issue:** #9, #39

### 2. Landing Page UI (High Priority)
- **Story:** As a user, I want to see a branded landing page so that I understand the application's purpose.
- **Tasks:**
    - Create landing page with Tree Hole Yale branding
    - Add sign up and sign in buttons
    - Include project description
    - Responsive design
- **Points:** 3
- **Issue:** #38

### 3. Sign Up Form UI with SSO Flow (High Priority)
- **Story:** As a user, I want a clear signup flow with SSO verification so that I can easily create an account.
- **Tasks:**
    - Create two-step signup form UI
    - Add step indicators
    - SSO redirect handling
    - Success/error messaging
    - Form validation feedback
- **Points:** 5
- **Issue:** #39

### 4. Profile & Activity Dashboard (Critical)
- **Story:** As a user, I want to view my profile and activity so that I can see my contributions.
- **Tasks:**
    - Create profile dashboard view
    - Display user information (name, email, school)
    - Show user statistics (posts created, votes received)
    - Activity timeline
    - Profile settings access
- **Points:** 8
- **Issue:** #32

### 5. View My Own Posts (High Priority)
- **Story:** As a user, I want to see all my posts so that I can manage my content.
- **Tasks:**
    - Create "My Posts" page
    - Filter posts by current user
    - Display post statistics
    - Edit/delete options (future)
- **Points:** 3
- **Issue:** #13

### 6. Settings Page (Critical)
- **Story:** As a user, I want to manage my account settings so that I can customize my experience.
- **Tasks:**
    - Create settings page UI
    - Email notification preferences
    - Change password functionality
    - Terms of Service and Privacy Policy pages
    - Help & Feedback form
    - FAQ section
- **Points:** 5
- **Issue:** #33, #44

### 7. Search & Tag Filtering Enhancement (High Priority)
- **Story:** As a user, I want to search posts and filter by tags so that I can find relevant content.
- **Tasks:**
    - Implement full-text search
    - Enhanced tag filtering with post counts
    - Search results page
    - Sort by recent or popularity
    - Debounced search input
- **Points:** 5
- **Issue:** #15

### 8. Upvote Posts (High Priority)
- **Story:** As a user, I want to upvote posts so that I can show appreciation for content.
- **Tasks:**
    - Create Vote model (if not exists)
    - Implement upvote view
    - AJAX upvote functionality
    - Update vote count display
    - Toggle behavior (unvote if already voted)
- **Points:** 3
- **Issue:** #17

### 9. Downvote Posts (High Priority)
- **Story:** As a user, I want to downvote posts so that I can express disagreement.
- **Tasks:**
    - Implement downvote view
    - AJAX downvote functionality
    - Net vote calculation
    - Toggle behavior
- **Points:** 3
- **Issue:** (Related to #17)

### 10. Tag Input Field & Hashtag Parsing (High Priority)
- **Story:** As a user, I want to add tags via input field or hashtags so that I can categorize my posts easily.
- **Tasks:**
    - Add tag input field to post form
    - Implement hashtag parsing from post body (#tag)
    - Real-time hashtag preview
    - Combine input tags and hashtags
    - Automatic tag creation
- **Points:** 5
- **Issue:** #41, #42

### 11. Authentication Flow E2E Tests (High Priority)
- **Story:** As a developer, I want comprehensive tests for authentication so that I can ensure reliability.
- **Tasks:**
    - Write end-to-end authentication tests
    - Test SSO flow (mock)
    - Test signup/login/logout
    - Test error cases
    - Achieve 100% coverage for auth flow
- **Points:** 5
- **Issue:** #47

## Team Assignments
- **Authentication Team:** SSO integration, signup flow (#9, #39, #47)
- **Profile Team:** Profile dashboard, settings, my posts (#32, #33, #13, #44)
- **Posting Team:** Tag enhancements, voting, search (#15, #17, #41, #42)
- **Frontend Team:** Landing page, UI improvements (#38)

## Risks & Mitigation
- **SSO Complexity:** Risk of SSO integration issues. Mitigation: Start with mock SSO, document production requirements.
- **Performance:** Risk of slow search with many posts. Mitigation: Use database indexes, implement debouncing.
- **Vote System:** Risk of race conditions. Mitigation: Use database transactions, handle edge cases.
- **Scope Creep:** Risk of adding too many features. Mitigation: Stick to planned stories, defer nice-to-haves.

## Definition of Done
- [ ] SSO authentication flow working (mock for dev, ready for production)
- [ ] Profile dashboard displays user information and statistics
- [ ] Settings page with all planned features
- [ ] Users can view their own posts
- [ ] Search functionality working with tag filtering
- [ ] Upvote and downvote functionality implemented
- [ ] Tag input and hashtag parsing working
- [ ] All features have automated tests
- [ ] Code reviewed and merged to main
- [ ] No critical bugs

## Sprint Backlog Summary
**Total Story Points:** 60 points
**Focus:** User experience enhancements and feature completeness
**Estimated Velocity:** 60 points (increased from Sprint 2's 45 points)

## Dependencies
- Sprint 2 authentication and posting features must be complete
- Database models from previous sprints must be stable
- Base templates and design system from Sprint 1

## Notes
- This sprint focuses on enhancing existing features and adding user management
- SSO integration is critical but can start with mock implementation
- Voting system needs careful design to prevent abuse
- Search functionality should be performant even with many posts
- Profile system is important for user engagement

---

**Planning Date:** Start of Week 5  
**Sprint Start:** Week 5  
**Sprint End:** Week 6
