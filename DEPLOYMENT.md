# Deployment Guide

This guide walks you through deploying the Todo Full-Stack Web Application with the frontend on **Vercel** and the backend on **Hugging Face Spaces**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Hugging Face Spaces)](#backend-deployment-hugging-face-spaces)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Testing the Deployment](#testing-the-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- **GitHub Account**: Your code should be pushed to a GitHub repository
- **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
- **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
- **Neon PostgreSQL Database**: Already configured with your `DATABASE_URL`
- **Environment Variables**: Ready from your `.env` files

### Required Environment Variables

**Backend:**
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token generation/validation

**Frontend:**
- `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend (Hugging Face Space URL)

---

## Backend Deployment (Hugging Face Spaces)

Hugging Face Spaces supports Docker-based deployments, which is perfect for FastAPI applications.

### Step 1: Create a Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure your Space:
   - **Owner**: Your username or organization
   - **Space name**: `todo-backend` (or your preferred name)
   - **License**: Choose appropriate license (e.g., MIT)
   - **Select the Space SDK**: Choose **Docker**
   - **Visibility**: Public or Private (your choice)
4. Click **"Create Space"**

### Step 2: Prepare Backend Files

Your backend needs a `Dockerfile` to run on Hugging Face Spaces. Create this file in your `backend/` directory (already created in the project).

### Step 3: Push Backend to Hugging Face Space

You have two options:

#### Option A: Using Git (Recommended)

```bash
# Navigate to your backend directory
cd backend

# Initialize git if not already done
git init

# Add Hugging Face Space as remote
# Replace YOUR_USERNAME and YOUR_SPACE_NAME
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Add all backend files
git add .

# Commit
git commit -m "Initial backend deployment"

# Push to Hugging Face
git push hf main
```

#### Option B: Using Hugging Face Web Interface

1. Go to your Space's **"Files"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload all files from your `backend/` directory:
   - `Dockerfile`
   - `requirements.txt`
   - All files in `src/` directory
   - `.env` (configure environment variables in Space settings instead - see Step 4)

### Step 4: Configure Environment Variables

1. In your Hugging Face Space, go to **"Settings"** tab
2. Scroll to **"Repository secrets"** section
3. Click **"New secret"**
4. Add the following secrets:
   - **Name**: `DATABASE_URL`
     **Value**: Your full Neon PostgreSQL connection string
   - **Name**: `BETTER_AUTH_SECRET`
     **Value**: Your JWT secret key (same as in development)

### Step 5: Wait for Build

1. Hugging Face will automatically build your Docker container
2. Check the **"Logs"** tab to monitor the build progress
3. Once complete, your backend will be accessible at:
   ```
   https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
   ```

### Step 6: Verify Backend is Running

Test your backend API:

```bash
# Replace with your actual Hugging Face Space URL
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/

# You should receive a JSON response like:
# {"message": "Todo API is running"}
```

---

## Frontend Deployment (Vercel)

Vercel provides seamless deployment for Next.js applications with automatic builds and deployments.

### Step 1: Push Code to GitHub

Ensure your code is in a GitHub repository:

```bash
# From your project root
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Import Project to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository:
   - Click **"Import"** next to your repository
   - If not listed, click **"Adjust GitHub App Permissions"** to grant access

### Step 3: Configure Project Settings

Vercel will detect it's a Next.js project automatically.

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: Click **"Edit"** and set to `frontend`
3. **Build and Output Settings**: Leave as default
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

### Step 4: Configure Environment Variables

1. Expand **"Environment Variables"** section
2. Add the following variable:
   - **Name**: `NEXT_PUBLIC_API_BASE_URL`
   - **Value**: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
     (Replace with your actual Hugging Face Space URL from backend deployment)
   - **Environment**: Select all (Production, Preview, Development)

### Step 5: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - Install dependencies
   - Build your Next.js application
   - Deploy to a production URL
3. Wait for the build to complete (usually 1-3 minutes)

### Step 6: Get Your Frontend URL

Once deployed, Vercel provides your production URL:
```
https://your-project-name.vercel.app
```

You can also configure a custom domain in **Settings** → **Domains**.

---

## Post-Deployment Configuration

### Update CORS Settings (Backend)

Your backend needs to allow requests from your Vercel frontend URL.

1. Update `backend/src/main.py` CORS origins:

```python
# Add your Vercel URL to allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-project-name.vercel.app"  # Add this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Commit and push changes to Hugging Face Space:

```bash
cd backend
git add src/main.py
git commit -m "Update CORS for production"
git push hf main
```

### Update Frontend Environment Variable (if needed)

If your Hugging Face Space URL changed:

1. Go to Vercel Dashboard → Your Project → **Settings** → **Environment Variables**
2. Edit `NEXT_PUBLIC_API_BASE_URL` to match your Hugging Face Space URL
3. **Redeploy** from **Deployments** tab

---

## Testing the Deployment

### 1. Test Backend API

```bash
# Health check
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/

# Test registration (example)
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

### 2. Test Frontend

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. Navigate to **Register** page
3. Create a new account
4. Sign in
5. Create, view, edit, and delete tasks
6. Verify all CRUD operations work

### 3. Test Multi-User Isolation

1. Open an incognito/private window
2. Register a different user
3. Verify each user only sees their own tasks

---

## Troubleshooting

### Backend Issues

**Problem**: Backend won't start on Hugging Face
- **Solution**: Check **Logs** tab in Hugging Face Space
- Verify `DATABASE_URL` is correctly set in secrets
- Ensure all dependencies are in `requirements.txt`

**Problem**: Database connection errors
- **Solution**: Verify your Neon PostgreSQL database is active
- Check that `DATABASE_URL` includes `?sslmode=require`
- Ensure database allows connections from Hugging Face IPs

**Problem**: CORS errors in browser console
- **Solution**: Add your Vercel URL to CORS allowed origins in `backend/src/main.py`

### Frontend Issues

**Problem**: Frontend can't connect to backend
- **Solution**: Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly in Vercel
- Check browser console for the exact API URL being called
- Ensure backend is running and accessible

**Problem**: Environment variable not updating
- **Solution**: After changing environment variables in Vercel, redeploy from **Deployments** tab
- Clear browser cache and hard reload

**Problem**: Build fails on Vercel
- **Solution**: Check build logs in Vercel dashboard
- Ensure `package.json` has all required dependencies
- Verify TypeScript has no errors: `npm run build` locally

### General Issues

**Problem**: 401 Unauthorized errors
- **Solution**: Ensure `BETTER_AUTH_SECRET` is the same in both frontend and backend
- Check that JWT tokens are being sent in request headers
- Verify token hasn't expired

**Problem**: White/blank page after deployment
- **Solution**: Check browser console for errors
- Verify all environment variables are set
- Check Vercel function logs for runtime errors

---

## Continuous Deployment

### Automatic Deployments

Both platforms support automatic deployments:

**Vercel**: Automatically redeploys when you push to your GitHub repository's main branch

**Hugging Face**: Automatically rebuilds when you push to the Space's git repository

### Manual Deployments

**Vercel**:
- Go to **Deployments** tab → Click **"Redeploy"** on any deployment

**Hugging Face**:
- Push changes via git, or use the web interface to edit files

---

## Production Checklist

Before going to production, ensure:

- [ ] Environment variables are set correctly on both platforms
- [ ] CORS origins include your Vercel frontend URL
- [ ] Database connection is secure (SSL enabled)
- [ ] `BETTER_AUTH_SECRET` is a strong, random string (not from development)
- [ ] Both frontend and backend are accessible via HTTPS
- [ ] Registration and login work correctly
- [ ] All CRUD operations function properly
- [ ] Multi-user data isolation is working
- [ ] Error messages are user-friendly (no sensitive info leaked)
- [ ] Performance is acceptable (check Vercel Analytics)

---

## Useful Commands

### Vercel CLI (Optional)

Install Vercel CLI for command-line deployments:

```bash
npm install -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Deploy to production
vercel --prod
```

### Hugging Face CLI (Optional)

```bash
# Install
pip install huggingface_hub

# Login
huggingface-cli login

# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

---

## Support and Resources

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Hugging Face Spaces**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Next.js Deployment**: [nextjs.org/docs/deployment](https://nextjs.org/docs/deployment)
- **FastAPI Deployment**: [fastapi.tiangolo.com/deployment/](https://fastapi.tiangolo.com/deployment/)

---

## Deployment URLs Template

After deployment, record your URLs here:

- **Frontend URL**: `https://_____________________.vercel.app`
- **Backend URL**: `https://_____________________.hf.space`
- **Database**: Neon PostgreSQL (already configured)

---

Congratulations! Your Todo Full-Stack Web Application is now deployed and accessible to users worldwide! 🎉
