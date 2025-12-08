# Sprint 1 Retrospective

**Sprint Duration:** Week 1-2 (Project Kickoff)  
**Team:** Glyz-Team (Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng)

## What Went Well ✅

### 1. Project Setup
- **Django Configuration:** Successfully set up Django 5.2 with proper project structure
- **Team Environment:** All team members were able to get the project running locally
- **Database Design:** Initial models (Post, Tag) were well-designed and extensible
- **Documentation:** Created comprehensive CONTRIBUTING.md early, which helped establish workflow

### 2. Team Collaboration
- **Clear Communication:** Established regular check-ins and communication channels
- **Workflow Agreement:** Team agreed on feature-based file organization early
- **Git Strategy:** Defined branching strategy and commit message conventions
- **Knowledge Sharing:** Team members helped each other with Django setup issues

### 3. Planning & Organization
- **Scope Definition:** Clear understanding of MVP features
- **Architecture Decisions:** Made key decisions about project structure upfront
- **Design System:** Established CSS structure and branding early
- **Issue Tracking:** Set up GitHub issues and project board

### 4. Technical Foundation
- **Code Organization:** Feature-based structure (models/, views/, forms/, tests/) established
- **Template Structure:** Base template with consistent navigation
- **Development Tools:** Virtual environment, requirements.txt, .gitignore all configured
- **Best Practices:** Followed Django conventions from the start

## What Could Be Improved 🔄

### 1. Time Management
- **Issue:** Some team members spent more time than expected on Django learning curve
- **Impact:** Slightly delayed start on some tasks
- **Action:** Create Django onboarding guide for future reference

### 2. Scope Clarity
- **Issue:** Initial uncertainty about exact feature scope
- **Impact:** Some rework on database schema
- **Action:** More detailed user stories needed for Sprint 2

### 3. Testing Setup
- **Issue:** Did not set up testing framework in Sprint 1
- **Impact:** Will need to add tests retroactively
- **Action:** Include test setup in Sprint 2 planning

### 4. Documentation
- **Issue:** Some technical decisions not fully documented
- **Impact:** Future reference may require code inspection
- **Action:** Add inline code comments and architecture notes

## Action Items for Sprint 2

### High Priority
1. ✅ **Set up testing framework** - Add Django test structure and initial tests
2. ✅ **Create detailed user stories** - Break down authentication and posting features
3. ✅ **Establish velocity baseline** - Track story points to establish team velocity
4. ✅ **Add inline documentation** - Document key architectural decisions

### Medium Priority
1. ✅ **Django onboarding guide** - Create quick reference for team members
2. ✅ **Code review process** - Define PR review guidelines
3. ✅ **Environment variables** - Set up .env file structure

### Low Priority
1. ✅ **CI/CD exploration** - Research automated testing/deployment options
2. ✅ **Performance monitoring** - Consider adding Django Debug Toolbar

## Key Learnings

### Technical
1. **Feature-based organization** prevents merge conflicts - this will be crucial for parallel development
2. **Base template early** makes UI development faster - all pages inherit consistent structure
3. **Django migrations** need careful planning - model changes require migration strategy

### Process
1. **Early documentation** saves time later - CONTRIBUTING.md helped align team
2. **Clear communication** is essential - regular check-ins prevented blockers
3. **Agile planning** works well - breaking work into small stories helps estimation

### Team
1. **Knowledge sharing** accelerates learning - team members helped each other
2. **Pair programming** useful for complex setup - helped resolve Django configuration issues
3. **Clear ownership** prevents duplicate work - feature-based structure enables parallel work

## Metrics & Velocity

- **Sprint Type:** Setup/Planning Sprint
- **Story Points:** 24 points (not counted in feature velocity)
- **Team Capacity:** 4 developers
- **Completion Rate:** 100% (all planned tasks completed)
- **Velocity Baseline:** To be established in Sprint 2

## Process Improvements

### For Next Sprint
1. **Daily Standups:** Implement brief daily check-ins (async or sync)
2. **Story Estimation:** Use planning poker for more accurate estimates
3. **Definition of Done:** Add checklist to each user story
4. **Test Coverage:** Set minimum test coverage requirement (e.g., 70%)

### Long-term
1. **Automated Testing:** Set up CI/CD pipeline
2. **Code Quality:** Add linting and formatting tools (black, flake8)
3. **Performance:** Monitor query performance from the start
4. **Security:** Include security review in Definition of Done

## Team Feedback

### Positive
- "Great foundation - I feel confident we can build features quickly now"
- "Feature-based organization is smart - prevents conflicts"
- "Clear documentation helped me get started quickly"

### Areas for Improvement
- "Would have liked more Django examples in the docs"
- "Some tasks took longer than expected - need better estimation"
- "Should have set up testing framework earlier"

## Retrospective Summary

**Overall:** Sprint 1 was successful in establishing a solid foundation for the project. The team worked well together, established good practices, and created a structure that will support rapid feature development in subsequent sprints.

**Key Success:** Feature-based file organization and early documentation will pay dividends in future sprints.

**Main Focus for Sprint 2:** Begin feature development with authentication and basic posting, while maintaining the quality and organization established in Sprint 1.

---

**Retrospective Date:** End of Week 2  
**Next Sprint:** Sprint 2 - Authentication & Basic Posting
