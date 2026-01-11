---
id: 1
title: Update Hackathon Constitution
stage: constitution
date_iso: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude Code
command: sp.constitution
labels: ["constitution", "hackathon", "spec-driven-development", "cloud-native"]
spec: null
ticket: null
adr: null
pr: null
outcome: Completed
evaluation: Successful constitution update with all principles and guidelines from hackathon requirements
---

# Update Hackathon Constitution

## Files Modified
 - C:\Users\haroon traders\Desktop\hackathon-2\phase-2\.specify\memory\constitution.md

## Tests Run
 - None

## Prompt Text
```
# Project Constitution

Project: Hackathon II - The Evolution of Todo: Mastering Spec-Driven Development & Cloud Native AI

## Core Principles
- Spec-Driven Development: All implementations must start with detailed specifications refined through iterations with Claude Code.
- No Manual Coding: Code generation must be handled exclusively by Claude Code; refine specs until the output is correct.
- Iterative Evolution: Build the application progressively from a simple console app to a cloud-native AI chatbot, incorporating reusable intelligence and AI agents.
- Cloud-Native Focus: Emphasize containerization, orchestration, event-driven architecture, and AIOps.
- Reusable Intelligence: Develop and utilize agent skills and subagents for modular, intelligent components.
- Agentic Dev Stack: Follow the workflow of writing specs, generating plans, breaking into tasks, and implementing via Claude Code.

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

## Success Criteria
- Complete All Phases: Fully functional implementations for each phase, demonstrating feature progression.
- Working Deployments: Successful local and cloud deployments with accessible URLs.
- AI Functionality: Chatbot handles natural language commands effectively using MCP tools.
- Event-Driven Features: Proper integration of Kafka/Dapr for advanced functionalities like reminders and recurring tasks.
- Bonus Implementations: Optional extras like reusable intelligence, multi-language support, voice commands for additional points.
- Zero Manual Code: All code traceable to Claude Code generations.
- High-Quality Specs: Specs refined to produce correct, efficient implementations.

## Phases

### Phase I: Todo In-Memory Python Console App
- **Objective**: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.
- **Functionality**: Implement Basic Level features - Add Task, Delete Task, Update Task, View Task List, Mark as Complete.
- **Development Approach**: Use Agentic Dev Stack; no manual coding.
- **Requirements**:
  - Add tasks with title and description.
  - List all tasks with status indicators.
  - Update task details.
  - Delete tasks by ID.
  - Mark tasks as complete/incomplete.
  - Follow clean code principles and proper Python project structure.
- **Technology Stack**: UV, Python 3.13+, Claude Code, Spec-Kit Plus.
- **Deliverables**:
  - GitHub repository with constitution file, specs history folder, /src folder with Python source code, README.md with setup instructions, CLAUDE.md with Claude Code instructions.
  - Working console application demonstration.
- **WSL 2 Setup for Windows Users**: Required for development.

### Phase II: Todo Full-Stack Web Application
- **Objective**: Transform the console app into a modern multi-user web application with persistent storage using Claude Code and Spec-Kit Plus.
- **Functionality**: Implement Basic Level features as a web app.
- **Development Approach**: Use Agentic Dev Stack; no manual coding.
- **Requirements**:
  - Create RESTful API endpoints.
  - Build responsive frontend interface.
  - Store data in Neon Serverless PostgreSQL database.
  - Implement user signup/signin using Better Auth.
  - Secure API with JWT tokens for user isolation.
- **Technology Stack**:
  - Frontend: Next.js 16+ (App Router).
  - Backend: Python FastAPI.
  - ORM: SQLModel.
  - Database: Neon Serverless PostgreSQL.
  - Spec-Driven: Claude Code + Spec-Kit Plus.
  - Authentication: Better Auth.
- **API Endpoints**:
  - GET /api/{user_id}/tasks: List all tasks.
  - POST /api/{user_id}/tasks: Create a new task.
  - GET /api/{user_id}/tasks/{id}: Get task details.
  - PUT /api/{user_id}/tasks/{id}: Update a task.
  - DELETE /api/{user_id}/tasks/{id}: Delete a task.
  - PATCH /api/{user_id}/tasks/{id}/complete: Toggle completion.
- **Monorepo Structure**: Use Spec-Kit organized folder structure with .spec-kit/config.yaml, specs folder, frontend/backend subfolders, etc.
- **Deliverables**: Updated GitHub repo; deployed on Vercel with frontend URL and backend API URL.

### Phase III: Todo AI Chatbot
- **Objective**: Create an AI-powered chatbot interface for managing todos through natural language using MCP server architecture, Claude Code, and Spec-Kit Plus.
- **Functionality**: Implement conversational interface for all Basic Level features.
- **Development Approach**: Use Agentic Dev Stack; no manual coding.
- **Requirements**:
  - Use OpenAI Agents SDK for AI logic.
  - Build MCP server with Official MCP SDK exposing task operations as tools.
  - Stateless chat endpoint persisting conversation state to database.
  - AI agents use MCP tools to manage tasks; tools are stateless and store state in DB.
- **Technology Stack**:
  - Frontend: OpenAI ChatKit.
  - Backend: Python FastAPI.
  - AI Framework: OpenAI Agents SDK.
  - MCP Server: Official MCP SDK.
  - ORM: SQLModel.
  - Database: Neon Serverless PostgreSQL.
  - Authentication: Better Auth.
- **Architecture**: ChatKit UI → FastAPI Server (Chat Endpoint → OpenAI Agents SDK → MCP Server) ↔ Neon DB.
- **Database Models**:
  - Task: user_id, id, title, description, completed, created_at, updated_at.
  - Conversation: user_id, id, created_at, updated_at.
  - Message: user_id, id, conversation_id, role (user/assistant), content, created_at.
- **Chat API Endpoint**: POST /api/{user_id}/chat - Send message & get AI response.
- **MCP Tools**: add_task, list_tasks, complete_task, delete_task, update_task with specified parameters and returns.
- **Agent Behavior**: Specific responses for task creation, listing, completion, deletion, update, confirmation, error handling.
- **Deliverables**: Updated repo; chatbot URL.

### Phase IV: Local Kubernetes Deployment (Minikube, Helm Charts, kubectl-ai, Kagent, Docker Desktop, and Gordon)
- **Objective**: Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube and Helm Charts.
- **Functionality**: Cloud Native Todo Chatbot with Basic Level Functionality.
- **Development Approach**: Use Agentic Dev Stack; no manual coding.
- **Requirements**:
  - Containerize frontend and backend applications (use Gordon if available).
  - Use Docker AI Agent (Gordon) for AI-assisted Docker operations.
  - Create Helm charts for deployment (use kubectl-ai and/or kagent to generate).
  - Use kubectl-ai and kagent for AI-assisted Kubernetes operations.
  - Deploy on Minikube locally.
- **Technology Stack**:
  - Containerization: Docker (Docker Desktop).
  - Docker AI: Docker AI Agent (Gordon).
  - Orchestration: Kubernetes (Minikube).
  - Package Manager: Helm Charts.
  - AI DevOps: kubectl-ai, Kagent.
  - Application: Phase III Todo Chatbot.
- **AIOps**: Use Gordon for Docker, kubectl-ai/kagent for Kubernetes commands.
- **Research Note**: Explore blueprints for spec-driven deployment.
- **Deliverables**: Instructions for local Minikube setup.

### Phase V: Advanced Cloud Deployment
- **Objective**: Implement advanced features and deploy to production-grade Kubernetes on Azure/Google Cloud/Oracle with Kafka or alternative Pub/Sub.
- **Functionality**: Advanced Level on cloud.
- **Development Approach**: Use Agentic Dev Stack; no manual coding.
- **Part A: Advanced Features**:
  - Implement all Advanced Level features (Recurring Tasks, Due Dates & Reminders).
  - Implement Intermediate Level features (Priorities, Tags, Search, Filter, Sort).
  - Add event-driven architecture with Kafka.
  - Implement Dapr for distributed application runtime.
- **Part B: Local Deployment**:
  - Deploy to Minikube.
  - Deploy Dapr on Minikube using Full Dapr (Pub/Sub, State, Bindings (cron), Secrets, Service Invocation).
- **Part C: Cloud Deployment**:
  - Deploy to Azure (AKS)/Google Cloud (GKE)/Oracle (OKE).
  - Deploy Dapr on cluster using Full Dapr.
  - Use Kafka on Confluent/Redpanda Cloud or alternative Pub/Sub with Dapr.
  - Set up CI/CD pipeline using GitHub Actions.
  - Configure monitoring and logging.
- **Cloud Setups**:
  - Microsoft Azure (AKS): $200 credits; create cluster, configure kubectl, deploy Helm charts.
  - Oracle Cloud (Always Free): Create OKE cluster (4 OCPUs, 24GB RAM).
  - Google Cloud (GKE): $300 credits.
- **Kafka Use Cases**:
  - Reminder/Notification System.
  - Recurring Task Engine.
  - Activity/Audit Log.
  - Real-time Sync Across Clients.
- **Deliverables**: DigitalOcean/AKS/GKE/OKE deployment URL.

## Bonus Features
- Reusable Intelligence: Create and use reusable intelligence via Claude Code Subagents and Agent Skills (+200 points).
- Cloud-Native Blueprints: Create and use via Agent Skills (+200 points).
- Multi-language Support: Support Urdu in chatbot (+100 points).
- Voice Commands: Add voice input for todo commands (+200 points).
```

## Response Text
Updated the project constitution by replacing all template placeholders with the specific content for Hackathon II. The new constitution includes all core principles, key standards, constraints, success criteria, phases, and bonus features as specified. Added a Sync Impact Report at the top, proper versioning (1.0.0), and appropriate dates. The file was successfully written to .specify/memory/constitution.md.