# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `1-todo-fullstack-web` | **Date**: 2026-01-07 | **Spec**: [link to spec](../spec.md)

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase I console todo application into a complete, production-ready, multi-user web application with persistent storage, responsive UI, secure authentication, and RESTful API integration. This involves setting up a monorepo with Next.js frontend and FastAPI backend, implementing Better Auth for authentication, SQLModel for database models, and Neon Serverless PostgreSQL for storage.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**: FastAPI, Next.js 16+ (App Router), SQLModel, Better Auth, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL database
**Testing**: pytest (backend), Jest/Cypress (frontend)
**Target Platform**: Web application (Vercel deployment)
**Project Type**: Web (monorepo with frontend and backend)
**Performance Goals**: <2 seconds API response time, <3 seconds frontend load time
**Constraints**: JWT token authentication, user data isolation, persistent storage
**Scale/Scope**: Multi-user support, 100+ concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Spec-Driven Development: All implementations must start with detailed specifications refined through iterations with Claude Code
- No Manual Coding: Code generation must be handled exclusively by Claude Code; refine specs until the output is correct
- Iterative Evolution: Build the application progressively from a simple console app to a cloud-native AI chatbot
- Cloud-Native Focus: Emphasize containerization, orchestration, event-driven architecture
- Reusable Intelligence: Develop and utilize agent skills and subagents for modular components
- Agentic Dev Stack: Follow the workflow of writing specs, generating plans, breaking into tasks, and implementing via Claude Code

## Project Structure

### Documentation (this feature)
```text
specs/1-todo-fullstack-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── task_routes.py
│   ├── main.py
│   └── database.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── requirements.txt
└── alembic/

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   └── api/
│   │       └── auth/
│   │           └── client.ts
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── Navbar.tsx
│   ├── lib/
│   │   └── api.ts
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── tsconfig.json
└── next.config.js

.spec-kit/
├── config.yaml
└── templates/

specs/
└── 1-todo-fullstack-web/
    └── [spec files]

.env
README.md
CLAUDE.md
```

**Structure Decision**: Monorepo structure with separate frontend and backend directories as required by the hackathon specification. Backend uses FastAPI with SQLModel for database operations and Better Auth for authentication. Frontend uses Next.js 16+ with App Router for routing and UI components. This structure enables independent deployment while maintaining shared configuration and spec-driven development approach.

## Detailed Implementation Steps

### Phase 0: Monorepo Initialization
1. Initialize the monorepo structure with proper .spec-kit/config.yaml
2. Set up shared configuration files (.env, README.md, CLAUDE.md)
3. Configure development environments for both frontend and backend

### Phase 1: Database Schema Design
1. Define SQLModel models for User and Task entities
   - User model: id, email, created_at, updated_at (managed by Better Auth)
   - Task model: id, user_id (foreign key), title (required), description (optional), completed (boolean), created_at, updated_at
   - Implement proper relationships ensuring user isolation
2. Establish proper relationships and user_id for isolation
   - Foreign key relationship from Task.user_id to User.id
   - All queries must filter by authenticated user_id to ensure data isolation
3. Ensure proper timestamp fields for audit trails
   - created_at: timestamp when record was created
   - updated_at: timestamp when record was last modified
4. Database configuration
   - Neon Serverless PostgreSQL connection
   - Connection pooling and environment configuration
   - Migration setup using Alembic for schema evolution

### Phase 2: Authentication Integration
1. Configure Better Auth with JWT plugin
   - Set up BETTER_AUTH_SECRET environment variable shared between frontend and backend
   - Configure user registration, login, and logout flows
   - Enable JWT token generation with user_id claims
2. Set up FastAPI JWT verification middleware
   - Create middleware to extract and verify JWT tokens from Authorization header
   - Decode user_id from JWT payload for user-specific data filtering
   - Return 401 Unauthorized for invalid or missing tokens
3. Implement secure token handling and validation
   - Frontend: Store tokens securely and attach to API requests
   - Backend: Verify tokens independently without session storage (stateless)
   - Token expiration and refresh handling
4. User session management
   - Login/logout functionality on frontend
   - Token persistence and cleanup
   - Error handling for authentication failures

### Phase 3: API Endpoint Implementation
1. Generate all specified RESTful endpoints with user-specific routing
   - GET /api/{user_id}/tasks: List all tasks for authenticated user
   - POST /api/{user_id}/tasks: Create a new task for authenticated user
   - GET /api/{user_id}/tasks/{id}: Get task details for authenticated user
   - PUT /api/{user_id}/tasks/{id}: Update a task for authenticated user
   - DELETE /api/{user_id}/tasks/{id}: Delete a task for authenticated user
   - PATCH /api/{user_id}/tasks/{id}/complete: Toggle completion status
2. Implement data filtering by user_id for security
   - All endpoints must verify JWT token contains matching user_id
   - Query filters to ensure users only access their own data
   - Validation to prevent cross-user data access
3. Ensure all endpoints return 401 for invalid tokens
   - Authentication middleware on all protected endpoints
   - Proper error responses for unauthorized access attempts
   - Consistent error handling across all endpoints
4. API security measures
   - Input validation and sanitization
   - Rate limiting to prevent abuse
   - Proper HTTP status codes for all responses

### Phase 4: Frontend UI Components
1. Build responsive Next.js pages and components for auth
   - Register page: Email and password registration form
   - Login page: Email and password login form
   - Layout component: Main layout with navigation and authentication state
   - Protected routes: Ensure unauthenticated users are redirected to login
2. Create task list, create/edit forms with proper UX
   - TaskList component: Display tasks with completion status and actions
   - TaskForm component: Create and edit task with title and description
   - Individual task page: Detailed view and editing capabilities
   - Responsive design: Mobile-first approach for all screen sizes
3. Implement navigation and state management
   - Navigation bar: Links to different sections with authentication awareness
   - Loading states: Visual feedback during API calls
   - Error handling: Display user-friendly error messages
   - Form validation: Client-side validation before API submission
4. User experience enhancements
   - Real-time feedback for user actions
   - Smooth transitions and animations
   - Accessibility features (keyboard navigation, screen readers)
   - Dark/light mode support (optional enhancement)

### Phase 5: API Client Integration
1. Implement secure API calls from frontend with JWT attachment
   - Create API client utility with axios or fetch wrapper
   - Automatically attach JWT token to Authorization header
   - Handle token refresh for expired tokens
   - Implement retry logic for failed requests
2. Handle error responses and authentication states
   - Intercept 401 responses and redirect to login
   - Display appropriate error messages to users
   - Clear authentication state on token expiration
   - Implement proper error boundaries for API failures
3. Ensure proper user-specific data handling
   - Pass user_id in API paths as required by specification
   - Validate user context before making API calls
   - Handle user-specific data isolation on frontend
4. API integration patterns
   - React hooks for data fetching and mutation (useSWR, React Query)
   - Type-safe API calls with TypeScript interfaces
   - Centralized error handling and logging
   - Caching strategies for improved performance

### Phase 6: Deployment Setup
1. Prepare Vercel deployment configuration for frontend
   - Configure next.config.js for production deployment
   - Set up environment variables for BETTER_AUTH_URL
   - Configure build settings and output configuration
   - Set up custom domain or use Vercel-provided URL
2. Set up backend API exposure and connection to Neon DB
   - Deploy backend API to a cloud provider (e.g., Railway, Render, or cloud VM)
   - Configure Neon PostgreSQL connection string for production
   - Set up SSL certificates and secure connections
   - Configure CORS to allow frontend domain access
3. Configure environment variables for production
   - BETTER_AUTH_SECRET: Shared secret for JWT validation
   - DATABASE_URL: Neon PostgreSQL connection string
   - Environment-specific configurations for dev/staging/prod
4. Deployment pipeline
   - GitHub Actions for CI/CD automation
   - Environment-specific deployments (dev, staging, prod)
   - Health checks and monitoring setup
   - Rollback procedures for failed deployments

### Phase 7: Quality Validation
1. Perform end-to-end testing for multi-user isolation
   - Create multiple user accounts and verify data separation
   - Test that users cannot access other users' tasks
   - Verify user-specific routing and data filtering
   - Validate JWT token user_id matches path user_id
2. Verify persistence across application restarts
   - Create tasks and verify they persist after backend restart
   - Test database connection reliability
   - Validate data integrity after deployment updates
   - Confirm Neon PostgreSQL maintains data consistently
3. Validate all security measures and authentication flows
   - Test unauthorized access attempts return 401
   - Verify JWT token validation works correctly
   - Confirm password security and hashing
   - Test session management and logout functionality
4. Performance and usability testing
   - API response times under normal load
   - Frontend loading performance on different devices
   - User experience validation for all core flows
   - Mobile responsiveness testing
5. Automated testing strategy
   - Unit tests for backend services and models
   - Integration tests for API endpoints
   - End-to-end tests for critical user journeys
   - Security tests for authentication and authorization

## Architectural Decisions

### 1. Monorepo Structure Decision
- **Decision**: Use monorepo with separate frontend and backend directories
- **Rationale**: Required by hackathon specification, enables better Spec-Kit integration and single-context Claude Code editing
- **Trade-offs**: Balances modularity with shared configuration; simplifies deployment coordination

### 2. Authentication Strategy
- **Decision**: Use Better Auth with JWT tokens for stateless authentication
- **Rationale**: Provides secure, standardized authentication; JWT allows independent backend verification without session storage
- **Trade-offs**: Better Auth handles user management securely while backend trusts decoded JWT user_id for task filtering

### 3. API Path Design
- **Decision**: Include explicit {user_id} in URL paths with JWT verification
- **Rationale**: Matches exact hackathon specification and adds defense-in-depth by matching JWT user_id against path
- **Trade-offs**: More verbose URLs but enhanced security through dual verification

### 4. Frontend Framework
- **Decision**: Use Next.js 16+ with App Router
- **Rationale**: Required by hackathon specification; provides modern routing, server components, and better performance
- **Trade-offs**: Learning curve for new features but superior for production applications

### 5. Database Integration
- **Decision**: Use SQLModel with Neon Serverless PostgreSQL
- **Rationale**: Aligns with specified tech stack; provides type safety and ORM capabilities
- **Trade-offs**: Abstraction layer over raw SQL but better maintainability and type safety

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All requirements align with constitution] |