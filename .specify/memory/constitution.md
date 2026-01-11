<!-- Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: All principles and sections from the provided constitution
Removed sections: Template placeholder comments
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Hackathon II - The Evolution of Todo: Mastering Spec-Driven Development & Cloud Native AI Constitution

## Core Principles

### Spec-Driven Development
All implementations must start with detailed specifications refined through iterations with Claude Code.

### No Manual Coding
Code generation must be handled exclusively by Claude Code; refine specs until the output is correct.

### Iterative Evolution
Build the application progressively from a simple console app to a cloud-native AI chatbot, incorporating reusable intelligence and AI agents.

### Cloud-Native Focus
Emphasize containerization, orchestration, event-driven architecture, and AIOps.

### Reusable Intelligence
Develop and utilize agent skills and subagents for modular, intelligent components.

### Agentic Dev Stack
Follow the workflow of writing specs, generating plans, breaking into tasks, and implementing via Claude Code.

## Key Standards

- Constitution and Specs: Write a Markdown constitution for the project and individual specs for every feature in each phase, stored in a specs history folder.
- Technology Adherence: Use specified stacks for each phase, including Python, Next.js, FastAPI, SQLModel, Neon DB, OpenAI tools, Docker, Kubernetes, etc.
- Authentication and Security: Implement user authentication with Better Auth and JWT tokens for API security.
- AI Integration: Use OpenAI Agents SDK, Official MCP SDK, and natural language processing for chatbot interactions.
- Deployment Blueprints: Develop and use cloud-native blueprints for spec-driven deployments.
- Evaluation Criteria: Processes, prompts, and iterations will be reviewed; all claims and implementations must be traceable to specs.
- Clean Code and Structure: Follow proper project structures, including monorepos with Spec-Kit configurations.

## Constraints

- Development Environment: Use WSL 2 on Windows; Python 3.13+, UV package manager.
- No Additional Tools: Stick to provided tech stacks; no unauthorized libraries or manual code writing.
- Feature Implementation: Must include all Basic, Intermediate, and Advanced features progressively across phases.
- Deployment Requirements: Local on Minikube for Phase IV; cloud on DigitalOcean, Azure, Google Cloud, or Oracle for Phase V.
- Submission Format: Public GitHub repo with constitution, specs, source code, README, CLAUDE.md; demo video under 90 seconds.
- Multi-User Support: Ensure applications handle multiple users with data isolation.
- Stateless Design: Chatbots and tools must be stateless, persisting state in the database.

## Governance

Success Criteria:
- Complete All Phases: Fully functional implementations for each phase, demonstrating feature progression.
- Working Deployments: Successful local and cloud deployments with accessible URLs.
- AI Functionality: Chatbot handles natural language commands effectively using MCP tools.
- Event-Driven Features: Proper integration of Kafka/Dapr for advanced functionalities like reminders and recurring tasks.
- Bonus Implementations: Optional extras like reusable intelligence, multi-language support, voice commands for additional points.
- Zero Manual Code: All code traceable to Claude Code generations.
- High-Quality Specs: Specs refined to produce correct, efficient implementations.

Phases:
- Phase I: Todo In-Memory Python Console App - Build a command-line todo application that stores tasks in memory
- Phase II: Todo Full-Stack Web Application - Transform into a modern multi-user web application with persistent storage
- Phase III: Todo AI Chatbot - Create an AI-powered chatbot interface for managing todos through natural language
- Phase IV: Local Kubernetes Deployment - Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube and Helm Charts
- Phase V: Advanced Cloud Deployment - Implement advanced features and deploy to production-grade Kubernetes

Bonus Features:
- Reusable Intelligence: Create and use reusable intelligence via Claude Code Subagents and Agent Skills (+200 points)
- Cloud-Native Blueprints: Create and use via Agent Skills (+200 points)
- Multi-language Support: Support Urdu in chatbot (+100 points)
- Voice Commands: Add voice input for todo commands (+200 points)

**Version**: 1.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07
