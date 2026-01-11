# Todo Full-Stack Web Application

## Overview
A multi-user todo application with Next.js frontend and FastAPI backend, featuring secure authentication and persistent storage.

## Features
- User registration and authentication
- Create, read, update, and delete tasks
- Multi-user data isolation
- Responsive web interface
- JWT-based security

## Tech Stack
- Frontend: Next.js 16+, TypeScript
- Backend: Python FastAPI, SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

## Setup
1. Clone the repository
2. Install dependencies for both frontend and backend
3. Set up environment variables
4. Run the development servers

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT validation
- `NEXTAUTH_URL`: Frontend URL for authentication callbacks

## Development
- Backend: `cd backend && uvicorn src.main:app --reload`
- Frontend: `cd frontend && npm run dev`

## Deployment

This application is designed for cloud deployment:

- **Frontend**: Vercel (Next.js optimized hosting)
- **Backend**: Hugging Face Spaces (Docker-based FastAPI deployment)
- **Database**: Neon Serverless PostgreSQL (already configured)

📘 **See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed step-by-step deployment instructions.**

### Quick Deployment Overview

1. **Backend (Hugging Face Spaces)**:
   - Create a new Space with Docker SDK
   - Push backend code to the Space
   - Configure environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
   - Access at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

2. **Frontend (Vercel)**:
   - Import GitHub repository to Vercel
   - Set root directory to `frontend`
   - Configure NEXT_PUBLIC_API_BASE_URL environment variable
   - Deploy with one click
   - Access at: `https://your-project-name.vercel.app`

For complete instructions with screenshots and troubleshooting, refer to [DEPLOYMENT.md](./DEPLOYMENT.md).