# Final Report - Tree Hole Yale

**Team**: Glyz-Team
**Members**: Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng
**Project**: Anonymous Yale-only Campus Forum
**Live URL**: https://glyz-team-tlug.onrender.com

---

## 1. Comprehensive Burndown/Velocity Chart

> **TODO**: Add burndown chart covering all 4 sprints showing story points planned vs completed

### Sprint Velocity Summary

| Sprint | Planned Story Points | Completed Story Points | Velocity | Completion Rate |
|--------|---------------------|------------------------|----------|-----------------|
| Sprint 1 | [TODO] | [TODO] | [TODO] | [TODO]% |
| Sprint 2 | [TODO] | [TODO] | [TODO] | [TODO]% |
| Sprint 3 | [TODO] | [TODO] | [TODO] | [TODO]% |
| Sprint 4 | [TODO] | [TODO] | [TODO] | [TODO]% |

**Average Velocity**: [TODO]
**Total Story Points Completed**: [TODO]

> **Note**: You can use tools like ZenHub, Screenful, or create custom charts from your GitHub Projects data.

---

## 2. Traffic & A/B Test Analysis

### A/B Test Endpoint Implementation

- **Endpoint URL**: `/972b69d/` (SHA1 hash of "Glyz-Team")
- **Button Variants Tested**:
  - Variant A: "kudos"
  - Variant B: "thanks"

### Analytics Results

> **TODO**: Add your analytics findings here

**Tracking Method**: [Specify what analytics tool you used - Google Analytics, self-rolled, etc.]

**Traffic Summary**:
- Total visitors to A/B test endpoint: [TODO]
- Variant A impressions: [TODO]
- Variant B impressions: [TODO]
- Button clicks (Variant A): [TODO]
- Button clicks (Variant B): [TODO]

**Preferred Variant**: [TODO - "kudos" or "thanks"]

**Analysis**: [TODO - Explain why you believe this variant was preferred based on your data]

---

## 3. Project Retrospective

### What Went Well Across All Sprints

Our team successfully delivered a functional, full-featured anonymous forum platform across 4 sprints. Key successes included:

1. **Responsive Design & Accessibility**
   - Built a platform that works seamlessly on both web and mobile devices
   - Ensured Yale students can access Tree Hole from any device, anywhere on campus

2. **Innovative AI-Powered Features**
   - Implemented AI-generated user profiles and avatars, allowing students to create unique anonymous identities
   - Developed AI-powered tag auto-generation that intelligently suggests relevant tags for posts
   - Built search functionality to help users find relevant discussions quickly
   - Laid groundwork for expanding tag intelligence as the platform grows

3. **Strong Team Collaboration**
   - Maintained excellent communication and coordination throughout all sprints
   - Leveraged innovative and fun discussions that combined human creativity with AI efficiency
   - Consistently met sprint deadlines and delivered planned features on time
   - Made effective use of AI/LLM tools (Claude, Cursor, GitHub Copilot) to accelerate development

4. **Successful Agile Practices**
   - Executed 4 complete sprints with planning, reviews, and retrospectives
   - Sprint ceremonies kept the team aligned and allowed for continuous improvement
   - Adapted well to changing requirements and technical challenges
   - Maintained clear user stories and task breakdowns in GitHub Projects

5. **Technical Achievements**
   - Successfully deployed both staging and production environments on Render
   - Implemented secure authentication with Yale email restriction
   - Built moderation tools for content management
   - Achieved proper separation of concerns with Django's MVC architecture
   - Integrated PostgreSQL for production-grade data persistence

### Challenges We Faced

While our team achieved significant successes, we also encountered several challenges:

1. **Deployment and Environment Issues**
   - Initial setup of staging and production environments on Render presented configuration challenges
   - Managing environment variables across local, staging, and production environments required careful attention
   - Database migrations occasionally caused issues between environments
   - Ensuring dev/prod parity according to 12-factor app principles took iteration

2. **Learning Curve with Django**
   - Team members had varying levels of experience with Django framework
   - Understanding Django's ORM, migrations, and template system required time investment
   - Navigating Django's project structure and app-based architecture was initially challenging
   - Implementing proper Django testing patterns required learning and adaptation

3. **AI/LLM Integration Difficulties**
   - While AI tools accelerated development, they occasionally generated code that needed significant refactoring
   - Balancing AI-generated code with our own understanding and code quality standards was challenging
   - AI tools sometimes made assumptions that didn't align with our specific Django patterns
   - Required careful review and testing of AI-suggested solutions to ensure they met our requirements

4. **Time Management Across Sprints**
   - Balancing the project with other coursework and commitments required discipline
   - Some sprints were more intense than others due to competing academic deadlines
   - Coordinating schedules for sprint planning and review meetings took effort

### What We Learned

This project provided invaluable learning experiences across multiple dimensions:

1. **Full-Stack Web Development**
   - Gained hands-on experience building a complete web application from database design to frontend implementation
   - Learned Django framework in depth, including models, views, templates, forms, and authentication
   - Understood how to structure a real-world web application for maintainability and scalability
   - Experienced the full development lifecycle from local development through production deployment

2. **Working with AI as a Development Tool**
   - Learned effective prompting techniques to get useful code from AI/LLMs
   - Understood when to trust AI suggestions vs when to apply human judgment
   - Discovered that AI tools are powerful accelerators but require human oversight and architectural guidance
   - Learned to use AI for code generation, debugging, documentation, and problem-solving

3. **Agile/Scrum Methodology in Practice**
   - Gained real experience with sprint planning, user stories, story points, and estimation
   - Understood the value of iterative development and continuous feedback loops
   - Learned how sprint retrospectives drive continuous improvement
   - Experienced how agile practices help teams adapt to changing requirements and discoveries

4. **Team Collaboration on Code**
   - Mastered git workflows including branching, pull requests, and code reviews
   - Learned to resolve merge conflicts and coordinate parallel development
   - Understood the importance of clear commit messages and documentation
   - Experienced how feature-based file organization minimizes merge conflicts

5. **12-Factor App Principles**
   - Learned how to build production-ready applications following industry best practices
   - Understood the importance of environment variables for configuration management
   - Gained experience with stateless processes and backing services
   - Learned about dev/prod parity and proper dependency management

6. **Software Engineering Best Practices**
   - Experienced the value of code reviews for maintaining quality
   - Learned how testing provides confidence in code changes
   - Understood the importance of documentation for team coordination
   - Gained appreciation for linting and code quality tools

### What We Would Do Differently Next Time

Reflecting on our experience, we identified several areas for improvement:

1. **Earlier Deployment Setup**
   - Would establish staging and production environments during Sprint 1, not later
   - Early deployment would have revealed environment-specific issues sooner
   - Could have practiced deployment workflows throughout the project rather than learning them late
   - Would reduce last-minute stress and allow more time for production testing

2. **More Testing from the Start**
   - Would write tests alongside feature development rather than adding them later
   - Test-driven development (TDD) would have caught bugs earlier in the development cycle
   - Earlier testing would have made refactoring safer and more confident
   - Would establish test coverage goals at the beginning and track them throughout

3. **Better Version Control Practices**
   - Would make smaller, more frequent commits for better change tracking
   - Would be more disciplined about branch naming and management
   - Would conduct more thorough code reviews before merging to main
   - Would establish clearer git workflow conventions in the team charter from day one

4. **More Realistic Initial Story Point Estimates**
   - Our early sprints had optimistic estimates that we adjusted over time
   - Would invest more time in breaking down user stories during Sprint 1 planning
   - Would have benefited from a "Sprint 0" to establish baseline velocity
   - Better estimates would have led to more predictable sprint outcomes

5. **Clearer AI Collaboration Guidelines**
   - Would establish team standards earlier for reviewing and integrating AI-generated code
   - Would define when to use AI tools vs when to write code manually
   - Would create patterns for effective prompting specific to our project's architecture
   - Clearer guidelines would have maintained more consistent code quality

6. **Documentation as We Go**
   - Would document architectural decisions and code patterns as we implement them
   - Would maintain a running list of "gotchas" and learnings for team reference
   - Better ongoing documentation would have reduced knowledge silos
   - Would have made onboarding and context switching easier

---

## Project Outcomes Summary

### Key Deliverables Achieved

✅ Fully functional anonymous forum platform
✅ Responsive design (web + mobile)
✅ AI-powered profile and avatar creation
✅ Search functionality
✅ AI tag auto-generation
✅ Secure Yale-only authentication
✅ Moderation tools and dashboard
✅ A/B test endpoint with analytics
✅ Both staging and production deployments
✅ Comprehensive sprint documentation
✅ Automated testing suite

### Technical Stack Delivered

- **Backend**: Django 5.2.8 (Python 3.12)
- **Database**: PostgreSQL (production), SQLite (local)
- **Frontend**: HTML, CSS, JavaScript with responsive design
- **Deployment**: Render (staging + production)
- **Version Control**: Git + GitHub with Projects V2
- **AI Integration**: Profile generation, avatar creation, tag suggestions

### Team Reflections

Working on Tree Hole Yale has been a transformative learning experience. We successfully combined human creativity with AI tools to build a meaningful platform for the Yale community. The project challenged us technically, taught us agile methodologies in practice, and gave us real experience building production software as a team.

Our greatest achievement was not just the technology we built, but learning how to work effectively as a software development team—planning together, solving problems collaboratively, and continuously improving our processes. These skills will serve us well in our future careers.

We're proud of what we've built and grateful for the opportunity to create something that could genuinely benefit Yale students.

---

**Report prepared by**: Glyz-Team
**Date**: December 2025
