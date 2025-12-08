# Sprint 2 Planning

**Sprint Goal:** Implement core authentication system and basic posting functionality to enable users to create accounts and post content.
**Duration:** Week 3-4

## Sprint Goal
By the end of Sprint 2, users will be able to sign up with Yale email validation, log in, create posts with titles and content, and view a feed of posts. This establishes the foundation for all future features.

## Selected User Stories

### 1. User Authentication - Sign Up (Critical)
- **Story:** As a new user, I want to sign up with my Yale email so that I can access the platform.
- **Tasks:**
    - Create signup form with username, email, password fields
    - Implement Yale email domain validation (@yale.edu)
    - Create user account in database
    - Handle form validation and error messages
    - Redirect to login after successful signup
- **Points:** 8
- **Issue:** #39, #40

### 2. User Authentication - Login (Critical)
- **Story:** As a registered user, I want to log in so that I can access my account.
- **Tasks:**
    - Create login form
    - Implement Django authentication
    - Handle login errors (invalid credentials)
    - Session management
    - Redirect to home after login
- **Points:** 5
- **Issue:** #39, #40

### 3. Post Creation Form (Critical)
- **Story:** As a logged-in user, I want to create a post with title and body so that I can share content.
- **Tasks:**
    - Create PostForm with title and body fields
    - Implement post creation view
    - Add anonymous posting option (checkbox)
    - Form validation (required fields, length limits)
    - Success message and redirect
- **Points:** 8
- **Issue:** #42

### 4. Home Feed View (Critical)
- **Story:** As a user, I want to see a feed of all posts so that I can browse content.
- **Tasks:**
    - Create home feed view
    - Display posts in reverse chronological order
    - Show post title, body, author (or anonymous), timestamp
    - Pagination (12 posts per page)
    - Handle empty state (no posts yet)
- **Points:** 5
- **Issue:** #41

### 5. Post Detail View (High Priority)
- **Story:** As a user, I want to click on a post to see its full content and details.
- **Tasks:**
    - Create post detail view
    - Display full post content
    - Show author information (if not anonymous)
    - Show creation timestamp
    - Navigation back to feed
- **Points:** 3
- **Issue:** #41

### 6. Tag System - Basic (High Priority)
- **Story:** As a user, I want to add tags to my posts so that content can be categorized.
- **Tasks:**
    - Extend Post model to support tags (ManyToMany relationship)
    - Add tag input field to post form
    - Create Tag model if not already done
    - Save tags when creating post
    - Display tags on post cards
- **Points:** 5
- **Issue:** #41

### 7. Tag Filtering (Medium Priority)
- **Story:** As a user, I want to filter posts by tag so that I can find relevant content.
- **Tasks:**
    - Add tag filter to home feed
    - Display available tags with post counts
    - Filter posts by selected tag
    - Clear filter option
- **Points:** 5
- **Issue:** #41

### 8. Basic Testing (High Priority)
- **Story:** As a developer, I want automated tests so that I can ensure features work correctly.
- **Tasks:**
    - Set up Django test framework
    - Write tests for authentication (signup, login)
    - Write tests for post creation
    - Write tests for tag functionality
    - Achieve minimum 70% test coverage
- **Points:** 6
- **Issue:** #47, #48, #49

## Team Assignments
- **Authentication Team:** Sign up and login features (#39, #40)
- **Posting Team:** Post creation, feed view, detail view (#41, #42)
- **Tag Team:** Tag system and filtering (#41)
- **Testing Team:** Test framework setup and initial tests (#47, #48, #49)

## Risks & Mitigation
- **Authentication Complexity:** Risk of security issues. Mitigation: Use Django's built-in authentication, follow security best practices.
- **Database Performance:** Risk of slow queries with many posts. Mitigation: Add database indexes, use pagination.
- **Tag Parsing:** Risk of tag input complexity. Mitigation: Start with simple comma-separated tags, enhance later.
- **Testing Coverage:** Risk of insufficient tests. Mitigation: Set minimum coverage requirement, review in code review.

## Definition of Done
- [ ] User can sign up with Yale email
- [ ] User can log in and log out
- [ ] User can create a post with title and body
- [ ] User can view feed of all posts
- [ ] User can view individual post details
- [ ] User can add tags to posts
- [ ] User can filter posts by tag
- [ ] All features have automated tests
- [ ] Code reviewed and merged to main
- [ ] No critical bugs or security issues

## Sprint Backlog Summary
**Total Story Points:** 45 points
**Focus:** Core authentication and posting functionality
**Estimated Velocity:** 45 points (first feature sprint)

## Dependencies
- Sprint 1 foundation must be complete
- Database models from Sprint 1 must be finalized
- Base templates from Sprint 1 must be ready

## Notes
- This is the first feature development sprint
- Focus on core functionality - polish can come later
- Testing is critical - establish good testing practices early
- Authentication is security-critical - extra care needed

---

**Planning Date:** Start of Week 3  
**Sprint Start:** Week 3  
**Sprint End:** Week 4
