# Deployment Checklist

Use this checklist to ensure a smooth deployment of your Todo Full-Stack Web Application.

## Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to GitHub repository
- [ ] No sensitive data (passwords, API keys) in code
- [ ] `.gitignore` properly configured
- [ ] All features tested locally
- [ ] No console errors or warnings

### 2. Database Setup
- [ ] Neon PostgreSQL database created
- [ ] Database connection string (DATABASE_URL) obtained
- [ ] Database is accessible (test connection)
- [ ] Tables created (via Alembic migrations or manual setup)

### 3. Environment Variables
- [ ] `BETTER_AUTH_SECRET` generated (use strong random string)
- [ ] All environment variables documented
- [ ] `.env.example` files created for reference

---

## Backend Deployment (Hugging Face Spaces)

### Hugging Face Account Setup
- [ ] Hugging Face account created
- [ ] Email verified

### Space Creation
- [ ] New Space created with Docker SDK
- [ ] Space name chosen (e.g., `todo-backend`)
- [ ] Visibility set (public or private)

### Code Deployment
- [ ] `Dockerfile` configured for port 7860
- [ ] `.dockerignore` file created
- [ ] Backend code pushed to Hugging Face Space
- [ ] Build completed successfully (check Logs tab)

### Environment Configuration
- [ ] `DATABASE_URL` added to Space secrets
- [ ] `BETTER_AUTH_SECRET` added to Space secrets
- [ ] Secrets saved and Space restarted

### Backend Verification
- [ ] Space is running (green status indicator)
- [ ] API accessible at Space URL
- [ ] Health endpoint returns 200 OK: `curl https://YOUR-SPACE.hf.space/`
- [ ] API documentation accessible: `/docs` and `/redoc`
- [ ] Database connection working (no errors in logs)

**Backend URL**: `https://________________________________.hf.space`

---

## Frontend Deployment (Vercel)

### Vercel Account Setup
- [ ] Vercel account created
- [ ] GitHub integration connected

### Project Import
- [ ] GitHub repository imported to Vercel
- [ ] Project name configured
- [ ] Root directory set to `frontend`
- [ ] Framework auto-detected as Next.js

### Build Configuration
- [ ] Build command: `npm run build` (default)
- [ ] Output directory: `.next` (default)
- [ ] Install command: `npm install` (default)
- [ ] Node.js version compatible (16.x or higher)

### Environment Variables
- [ ] `NEXT_PUBLIC_API_BASE_URL` added
- [ ] Variable value set to Hugging Face Space URL
- [ ] Environment set to all (Production, Preview, Development)

### Frontend Verification
- [ ] Build completed successfully
- [ ] No build errors or warnings
- [ ] Deployment succeeded
- [ ] Frontend accessible at Vercel URL
- [ ] No console errors in browser

**Frontend URL**: `https://________________________________.vercel.app`

---

## Integration Testing

### API Connection
- [ ] Frontend can connect to backend API
- [ ] No CORS errors in browser console
- [ ] API requests include proper headers

### Authentication Flow
- [ ] User registration works
- [ ] User login successful
- [ ] JWT token received and stored
- [ ] Protected routes require authentication
- [ ] Logout functionality works

### Task Management (CRUD)
- [ ] Create new task works
- [ ] View all tasks displays correctly
- [ ] Update task saves changes
- [ ] Delete task removes item
- [ ] Toggle task completion status works

### Multi-User Testing
- [ ] Register second user (different email)
- [ ] Each user sees only their own tasks
- [ ] No cross-user data access
- [ ] Data isolation verified

### Error Handling
- [ ] Invalid login shows error message
- [ ] Failed API calls display user-friendly errors
- [ ] 401 errors redirect to login
- [ ] Network errors handled gracefully

---

## Security Checklist

### Backend Security
- [ ] CORS configured with allowed origins
- [ ] Frontend URL added to CORS allowed origins
- [ ] JWT secret is strong and unique (not development key)
- [ ] Passwords are hashed (bcrypt)
- [ ] SQL injection protection via SQLModel
- [ ] Input validation on all endpoints

### Frontend Security
- [ ] No sensitive data in client-side code
- [ ] Environment variables use `NEXT_PUBLIC_` prefix correctly
- [ ] Security headers configured (vercel.json)
- [ ] XSS protection enabled
- [ ] HTTPS enforced (automatic on Vercel)

### Database Security
- [ ] Database uses SSL/TLS (Neon default)
- [ ] Connection string includes `?sslmode=require`
- [ ] Database credentials not exposed in code
- [ ] Only backend can access database

---

## Performance Checklist

### Backend
- [ ] API response times acceptable (< 2 seconds)
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Proper indexing on database tables

### Frontend
- [ ] Page load times acceptable (< 3 seconds)
- [ ] Images optimized (if any)
- [ ] No unnecessary re-renders
- [ ] Loading states implemented

### Monitoring
- [ ] Vercel Analytics enabled (optional)
- [ ] Error tracking configured (optional)
- [ ] Logs reviewed for issues

---

## Post-Deployment Tasks

### Documentation
- [ ] Deployment URLs recorded
- [ ] API documentation accessible
- [ ] README.md updated with deployment info
- [ ] DEPLOYMENT.md reviewed

### CORS Update
- [ ] Backend CORS includes production frontend URL
- [ ] Updated code pushed to Hugging Face Space
- [ ] Space rebuilt with new CORS settings

### User Acceptance Testing
- [ ] Full user flow tested end-to-end
- [ ] All features working in production
- [ ] Performance acceptable
- [ ] No breaking bugs

### Continuous Deployment
- [ ] Automatic deployments configured (GitHub → Vercel)
- [ ] Deployment notifications set up (optional)
- [ ] Rollback strategy understood

---

## Common Issues Resolved

- [ ] White screen / blank page → Check environment variables and build logs
- [ ] CORS errors → Verify backend CORS configuration includes frontend URL
- [ ] 401 errors → Ensure BETTER_AUTH_SECRET matches on frontend and backend
- [ ] Database errors → Verify DATABASE_URL is correct and database is accessible
- [ ] Build failures → Review build logs for specific errors

---

## Final Verification

- [ ] ✅ Backend deployed and accessible
- [ ] ✅ Frontend deployed and accessible
- [ ] ✅ Database connected and working
- [ ] ✅ Authentication functional
- [ ] ✅ CRUD operations working
- [ ] ✅ Multi-user isolation verified
- [ ] ✅ Security measures in place
- [ ] ✅ Performance acceptable
- [ ] ✅ No critical bugs

---

## Deployment Complete! 🎉

**Deployed Application:**
- Frontend: https://________________________________.vercel.app
- Backend: https://________________________________.hf.space
- Database: Neon PostgreSQL ✓

**Date Deployed**: ___________________

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________
