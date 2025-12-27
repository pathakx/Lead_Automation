# 🚀 RUN.md - How to Run the Lead Automation System

> **Quick guide to run the frontend and backend for testing**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Running the Backend](#running-the-backend)
4. [Running the Frontend](#running-the-frontend)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Testing Tools](#testing-tools)

---

## Prerequisites

Before running the project, ensure you have:

### Required Software
- ✅ **Python 3.11+** - For backend
- ✅ **Node.js 18+** and **npm** - For frontend
- ✅ **Git** - For version control

### Required API Keys
- ✅ **Supabase** - Database (URL, Anon Key, Service Key)
- ✅ **Groq** - AI categorization
- ✅ **Resend** - Email delivery

### How to Get API Keys

#### Supabase
1. Go to https://supabase.com
2. Create a new project
3. Go to **Settings** → **API**
4. Copy:
   - Project URL
   - `anon` `public` key
   - `service_role` `secret` key

#### Groq
1. Go to https://console.groq.com
2. Sign up/Login
3. Go to **API Keys**
4. Create new API key

#### Resend
1. Go to https://resend.com
2. Sign up/Login
3. Go to **API Keys**
4. Create new API key
5. Verify your sending domain (or use test mode)

---

## Environment Setup

### 1. Backend Environment Setup

Navigate to the backend directory:
```bash
cd lead-automation-backend
```

#### Create `.env` file

Copy the example file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

#### Edit `.env` file

Open `.env` in your text editor and fill in your API keys:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Groq AI Configuration
GROQ_API_KEY=gsk_...

# Resend Email Configuration
RESEND_API_KEY=re_...
RESEND_FROM_EMAIL=leads@yourdomain.com

# Application Configuration
APP_ENV=development
APP_NAME=Lead Automation System
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

#### Install Dependencies

Create and activate virtual environment:

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Frontend Environment Setup

Navigate to the frontend directory:
```bash
cd lead-automation-frontend
```

#### Create `.env` file

Copy the example file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

#### Edit `.env` file

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Backend API
VITE_API_URL=http://localhost:8000
```

#### Install Dependencies

```bash
npm install
```

---

## Running the Backend

### Step 1: Activate Virtual Environment

**Windows:**
```bash
cd lead-automation-backend
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd lead-automation-backend
source venv/bin/activate
```

### Step 2: Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['B:\\Project\\SaaS\\Second\\lead-automation-backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Verify Backend is Running

Open your browser and visit:
- **API Root**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/api/health

**Expected Response** (http://localhost:8000):
```json
{
  "message": "Lead Automation API",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Running the Frontend

### Step 1: Navigate to Frontend Directory

```bash
cd lead-automation-frontend
```

### Step 2: Start the Development Server

```bash
npm run dev
```

**Expected Output:**
```
  VITE v7.2.4  ready in 523 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 3: Open in Browser

Visit: **http://localhost:5173**

You should see the Lead Automation System homepage with the lead submission form.

---

## Verification

### ✅ Backend Verification Checklist

1. **API is accessible**:
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "environment": "development"
   }
   ```

2. **Swagger docs work**:
   - Visit http://localhost:8000/docs
   - You should see interactive API documentation

3. **Database connection**:
   - Backend logs should not show any Supabase connection errors

4. **AI service ready**:
   - No Groq API errors in logs

5. **Email service ready**:
   - No Resend API errors in logs

---

### ✅ Frontend Verification Checklist

1. **Page loads successfully**:
   - No console errors in browser DevTools (F12)

2. **Form is visible**:
   - Lead submission form displays correctly

3. **API connection**:
   - Open browser DevTools → Network tab
   - Submit a test lead
   - Should see POST request to `http://localhost:8000/api/leads`

---

### ✅ End-to-End Test

**Test the complete workflow:**

1. **Open frontend**: http://localhost:5173

2. **Fill out the lead form**:
   - Name: Test User
   - Email: test@example.com
   - Phone: 1234567890
   - Company: Test Company
   - Role: Architect
   - Products: Select 2-3 products
   - Message: "Need urgent quote for project"

3. **Submit the form**

4. **Check backend logs**:
   ```
   INFO: POST /api/leads - 200 OK
   INFO: AI categorization completed for lead_id: ...
   INFO: Email sent successfully to test@example.com
   ```

5. **Check Supabase**:
   - Go to Supabase dashboard
   - Table Editor → `leads` table
   - You should see the new lead entry

6. **Check email**:
   - Go to Resend dashboard: https://resend.com/emails
   - You should see the acknowledgement email sent

---

## Troubleshooting

### Backend Issues

#### Issue: `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Make sure you're in the backend directory
cd lead-automation-backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### Issue: `supabase.lib.client_options.ClientOptions() got an unexpected keyword argument`

**Solution:**
Update Supabase package:
```bash
pip install --upgrade supabase
```

---

#### Issue: Backend starts but API returns 500 errors

**Solution:**
1. Check `.env` file has all required variables
2. Verify API keys are correct
3. Check backend logs for specific error messages
4. Test database connection:
   ```python
   python -c "from app.utils.db import supabase; print('DB Connected:', supabase)"
   ```

---

#### Issue: CORS errors when frontend calls backend

**Solution:**
1. Check `CORS_ORIGINS` in backend `.env`:
   ```env
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```
2. Restart backend server

---

### Frontend Issues

#### Issue: `npm install` fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules & del package-lock.json  # Windows

# Reinstall
npm install
```

---

#### Issue: Frontend shows blank page

**Solution:**
1. Open browser DevTools (F12) → Console
2. Check for errors
3. Common fixes:
   ```bash
   # Clear Vite cache
   rm -rf node_modules/.vite  # Linux/Mac
   rmdir /s node_modules\.vite  # Windows
   
   # Restart dev server
   npm run dev
   ```

---

#### Issue: API calls fail with network error

**Solution:**
1. Verify backend is running on http://localhost:8000
2. Check `VITE_API_URL` in frontend `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
3. Restart frontend dev server (Vite needs restart for .env changes)

---

#### Issue: Environment variables not loading

**Solution:**
1. Ensure `.env` file is in the root of `lead-automation-frontend` directory
2. Variables must start with `VITE_`
3. Restart dev server (required for .env changes)

---

## Testing Tools

### 1. Email Delivery Verification

Test all email templates:

```bash
cd lead-automation-backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

python verify_email_delivery.py your-email@gmail.com
```

This will send test emails for all 5 templates.

---

### 2. Unit Tests

Run backend unit tests:

```bash
cd lead-automation-backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run all tests
pytest

# Run specific test file
pytest tests/test_email_service.py

# Run with coverage
pytest --cov=app tests/
```

---

### 3. API Testing with Swagger

1. Start backend server
2. Visit http://localhost:8000/docs
3. Test endpoints interactively:
   - Click on any endpoint
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"

---

### 4. Database Inspection

**Using Supabase Dashboard:**
1. Go to https://supabase.com
2. Open your project
3. Go to **Table Editor**
4. View tables:
   - `leads` - All submitted leads
   - `lead_products` - Products selected per lead
   - `lead_activity` - All activities (AI results, emails, etc.)
   - `assignments` - Lead assignments to sales team

**Using SQL Editor:**
```sql
-- View recent leads
SELECT * FROM leads ORDER BY created_at DESC LIMIT 10;

-- View lead with all activities
SELECT 
  l.name,
  l.email,
  l.priority,
  la.type,
  la.created_at
FROM leads l
LEFT JOIN lead_activity la ON l.id = la.lead_id
WHERE l.id = 'your-lead-id'
ORDER BY la.created_at;
```

---

## Quick Reference

### Backend Commands

```bash
# Start backend
cd lead-automation-backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload

# Run tests
pytest

# Run email verification
python verify_email_delivery.py test@example.com
```

### Frontend Commands

```bash
# Start frontend
cd lead-automation-frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Both Running Simultaneously

**Terminal 1 (Backend):**
```bash
cd lead-automation-backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd lead-automation-frontend
npm run dev
```

---

## Production Deployment

For production deployment instructions, see:
- Backend: `lead-automation-backend/README.md`
- Frontend: `lead-automation-frontend/README.md`
- Full guide: `PROJECT_IMPLEMENTATION_PLAN.md`

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Project Plan**: `PROJECT_IMPLEMENTATION_PLAN.md`
- **Quick Start**: `QUICK_START.md`
- **Email Testing**: `EMAIL_VERIFICATION_GUIDE.md`
- **Database Schema**: `database_schema.sql`

---

## Support

If you encounter issues:

1. **Check logs**: Backend terminal and browser console (F12)
2. **Verify environment**: All `.env` variables are set correctly
3. **Check API keys**: Test each service individually
4. **Review documentation**: Check relevant README files
5. **Database**: Verify Supabase connection and schema

---

**Happy Testing! 🚀**
