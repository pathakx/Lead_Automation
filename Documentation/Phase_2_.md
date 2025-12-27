# Phase 2: Project Setup & Infrastructure - Master Plan
## AI-Powered Lead Management Automation System

---

## 📅 Timeline: Days 2-3
**Status**: 🚀 Ready for Implementation  
**Last Updated**: December 26, 2024  
**Prerequisites**: Phase 1 completed and approved

---

## 🎯 Phase 2 Objectives

### Primary Goal
Set up the complete development environment and project infrastructure for both frontend and backend applications, ensuring all tools, dependencies, and configurations are properly initialized and ready for development.

### Success Criteria
- ✅ Frontend React application initialized and running
- ✅ Backend FastAPI application initialized and running
- ✅ All dependencies installed without errors
- ✅ Environment variables configured for all services
- ✅ Git repositories created with proper .gitignore
- ✅ Project folder structure established
- ✅ Health check endpoints working
- ✅ Development servers accessible (frontend: 5173, backend: 8000)

---

## 📋 Deliverables

### 1. Frontend Application Setup
- ✅ React + Vite + TypeScript project initialized
- ✅ TailwindCSS configured for styling
- ✅ Required npm packages installed
- ✅ Project folder structure created
- ✅ Environment variables configured
- ✅ Dev server running on `http://localhost:5173`

### 2. Backend Application Setup
- ✅ Python FastAPI project initialized
- ✅ Virtual environment created and activated
- ✅ All Python dependencies installed
- ✅ Project folder structure created
- ✅ Environment variables configured
- ✅ Dev server running on `http://localhost:8000`

### 3. External Service Accounts
- ✅ Supabase project created
- ✅ Groq API account setup
- ✅ Resend email account setup
- ✅ API keys obtained and secured

### 4. Version Control
- ✅ Git initialized for both projects
- ✅ .gitignore configured properly
- ✅ Initial commit created
- ✅ Remote repositories connected (optional)

### 5. Documentation
- ✅ README.md for both projects
- ✅ Setup instructions documented
- ✅ Environment variable templates created

---

## 🏗️ Project Structure

### Frontend Structure
```
lead-automation-frontend/
├── public/                    # Static assets
├── src/
│   ├── assets/               # Images, fonts, etc.
│   ├── components/           # Reusable React components
│   │   └── .gitkeep
│   ├── pages/                # Page components
│   │   └── .gitkeep
│   ├── services/             # API clients
│   │   ├── api.ts           # Backend API client
│   │   └── supabase.ts      # Supabase client
│   ├── hooks/                # Custom React hooks
│   │   └── .gitkeep
│   ├── types/                # TypeScript types
│   │   └── .gitkeep
│   ├── utils/                # Utility functions
│   │   └── .gitkeep
│   ├── App.tsx               # Main app component
│   ├── main.tsx              # Entry point
│   ├── index.css             # Global styles
│   └── vite-env.d.ts         # Vite types
├── .env                      # Environment variables (not committed)
├── .env.example              # Environment template
├── .gitignore
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
├── vite.config.ts
└── README.md
```

### Backend Structure
```
lead-automation-backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Settings & environment
│   ├── models/               # Pydantic models
│   │   ├── __init__.py
│   │   ├── lead.py
│   │   ├── activity.py
│   │   └── assignment.py
│   ├── services/             # Business logic services
│   │   ├── __init__.py
│   │   ├── ai_service.py     # Groq integration
│   │   ├── email_service.py  # Resend integration
│   │   ├── lead_service.py   # Lead business logic
│   │   └── scheduler_service.py
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── leads.py
│   │   ├── approvals.py
│   │   └── analytics.py
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── db.py             # Supabase client
│       └── helpers.py
├── tests/                    # Unit tests
│   └── __init__.py
├── .env                      # Environment variables (not committed)
├── .env.example              # Environment template
├── .gitignore
├── requirements.txt
├── README.md
└── venv/                     # Virtual environment (not committed)
```

---

## 📝 Detailed Implementation Steps

## DAY 2: Backend Setup & External Services

### Step 1: Create Supabase Project (30 minutes)

**Objective**: Set up PostgreSQL database on Supabase

**Tasks**:
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up / Log in
3. Click "New Project"
4. Configure project:
   - **Name**: `lead-automation-db`
   - **Database Password**: Generate strong password (save securely!)
   - **Region**: Choose closest to India (Mumbai/Singapore)
   - **Pricing Plan**: Free tier (sufficient for development)
5. Wait for project provisioning (~2 minutes)
6. Navigate to **Settings** → **API**
7. Copy these credentials:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhb...` (long JWT token)
   - **service_role key**: `eyJhb...` (different token - KEEP SECRET!)
8. Save credentials in password manager

**Verification**:
- [ ] Supabase project dashboard accessible
- [ ] Database is active (green status)
- [ ] API keys copied and saved

**Common Issues**:
- Project stuck on "Setting up database" → Wait 5 minutes, refresh
- Can't find API keys → Go to Settings → API (left sidebar)

---

### Step 2: Create Groq API Account (15 minutes)

**Objective**: Set up AI API for lead categorization

**Tasks**:
1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up with Google/GitHub account
3. Verify email if required
4. Navigate to **API Keys** section
5. Click "Create API Key"
6. Name: `lead-automation-dev`
7. Copy the key immediately (shows only once!)
8. Save in password manager

**Free Tier Limits** (as of 2024):
- 14,400 requests/day
- Sufficient for development and initial production

**Verification**:
- [ ] API key copied and saved
- [ ] Test key validity (we'll do this in Step 8)

**Fallback**: If Groq signup fails, use OpenAI API temporarily (will need code changes)

---

### Step 3: Create Resend Email Account (15 minutes)

**Objective**: Set up transactional email service

**Tasks**:
1. Go to [https://resend.com](https://resend.com)
2. Sign up with email
3. Verify email address
4. Navigate to **API Keys**
5. Click "Create API Key"
6. Name: `lead-automation-dev`
7. Copy the key (starts with `re_...`)
8. Save in password manager

**Email Setup**:
- For development: Use Resend's test domain `onboarding@resend.dev`
- For production: Will need to verify custom domain (Phase 8)

**Verification**:
- [ ] API key copied and saved
- [ ] Test domain available

---

### Step 4: Initialize Backend Project (45 minutes)

**Objective**: Create Python FastAPI project structure

**Commands** (Run in terminal):

```powershell
# Navigate to project root
cd b:\Project\SaaS\Second

# Create backend directory
mkdir lead-automation-backend
cd lead-automation-backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If execution policy error, run:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Upgrade pip
python -m pip install --upgrade pip

# Install core dependencies
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install supabase==2.3.0
pip install groq==0.4.0
pip install resend==0.7.0
pip install apscheduler==3.10.4
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0

# Generate requirements.txt
pip freeze > requirements.txt
```

**Create Project Structure**:

```powershell
# Create directory structure
mkdir app
mkdir app\models
mkdir app\services
mkdir app\api
mkdir app\utils
mkdir tests

# Create __init__.py files (makes directories Python packages)
New-Item -Path app\__init__.py -ItemType File
New-Item -Path app\models\__init__.py -ItemType File
New-Item -Path app\services\__init__.py -ItemType File
New-Item -Path app\api\__init__.py -ItemType File
New-Item -Path app\utils\__init__.py -ItemType File
New-Item -Path tests\__init__.py -ItemType File
```

**Verification**:
```powershell
# Check virtual environment is activated (should show (venv) in prompt)
# Check Python version
python --version  # Should be 3.9+

# Check installed packages
pip list
```

- [ ] Virtual environment created and activated
- [ ] All packages installed without errors
- [ ] Directory structure created

---

### Step 5: Create Backend Configuration Files (30 minutes)

**File 1: `.env.example` (Template)**

Create `b:\Project\SaaS\Second\lead-automation-backend\.env.example`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Resend Email Configuration
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=leads@yourdomain.com

# Application Configuration
APP_ENV=development
APP_NAME=Lead Automation System
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**File 2: `.env` (Actual - NOT committed to Git)**

Create `b:\Project\SaaS\Second\lead-automation-backend\.env`:

```env
# Supabase Configuration
SUPABASE_URL=<PASTE_YOUR_SUPABASE_URL>
SUPABASE_ANON_KEY=<PASTE_YOUR_ANON_KEY>
SUPABASE_SERVICE_KEY=<PASTE_YOUR_SERVICE_KEY>

# Groq AI Configuration
GROQ_API_KEY=<PASTE_YOUR_GROQ_KEY>

# Resend Email Configuration
RESEND_API_KEY=<PASTE_YOUR_RESEND_KEY>
RESEND_FROM_EMAIL=onboarding@resend.dev

# Application Configuration
APP_ENV=development
APP_NAME=Lead Automation System
CORS_ORIGINS=http://localhost:5173

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**File 3: `.gitignore`**

Create `b:\Project\SaaS\Second\lead-automation-backend\.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
```

**File 4: `app/config.py` (Settings Management)**

Create `b:\Project\SaaS\Second\lead-automation-backend\app\config.py`:

```python
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Groq AI
    GROQ_API_KEY: str
    
    # Resend Email
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "leads@yourdomain.com"
    
    # Application
    APP_ENV: str = "development"
    APP_NAME: str = "Lead Automation System"
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
```

**Verification**:
```powershell
# Test config loading
python -c "from app.config import settings; print(settings.APP_NAME)"
# Should print: Lead Automation System
```

- [ ] All config files created
- [ ] .env populated with real API keys
- [ ] Config loading works without errors

---

### Step 6: Create Basic FastAPI Application (30 minutes)

**File: `app/main.py`**

Create `b:\Project\SaaS\Second\lead-automation-backend\app\main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-Powered Lead Management Automation System",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "message": "Lead Automation API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.APP_ENV
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "supabase": "pending",  # Will test in Phase 3
            "groq": "pending",      # Will test in Phase 4
            "resend": "pending"     # Will test in Phase 4
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Auto-reload on code changes
    )
```

**Run the Backend**:

```powershell
# Make sure virtual environment is activated
# Navigate to backend directory
cd b:\Project\SaaS\Second\lead-automation-backend

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Test the API**:

Open browser and visit:
- http://localhost:8000 → Should see JSON response
- http://localhost:8000/health → Should see health status
- http://localhost:8000/docs → Should see Swagger UI (interactive API docs)

**Verification**:
- [ ] Server starts without errors
- [ ] Root endpoint returns JSON
- [ ] Health check endpoint works
- [ ] Swagger docs accessible at /docs

---

### Step 7: Create Backend README (15 minutes)

**File: `README.md`**

Create `b:\Project\SaaS\Second\lead-automation-backend\README.md`:

```markdown
# Lead Automation Backend

FastAPI backend for AI-powered lead management system.

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.9+
- **Database**: Supabase (PostgreSQL)
- **AI**: Groq (Llama 3.1 70B)
- **Email**: Resend
- **Scheduler**: APScheduler

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```powershell
cp .env.example .env
```

Required environment variables:
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_KEY
- GROQ_API_KEY
- RESEND_API_KEY

### 4. Run Development Server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

## API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── main.py          # FastAPI app entry
├── config.py        # Settings
├── models/          # Pydantic models
├── services/        # Business logic
├── api/             # Route handlers
└── utils/           # Utilities
```

## Development

- Phase 2: Infrastructure setup ✅
- Phase 3: Database schema (next)
- Phase 4: API endpoints
- Phase 5: AI integration
```

**Verification**:
- [ ] README.md created with setup instructions

---

## DAY 3: Frontend Setup

### Step 8: Initialize Frontend Project (45 minutes)

**Commands** (Run in new terminal):

```powershell
# Navigate to project root
cd b:\Project\SaaS\Second

# Create Vite React TypeScript project
npm create vite@latest lead-automation-frontend -- --template react-ts

# Navigate to frontend directory
cd lead-automation-frontend

# Install dependencies
npm install

# Install additional packages
npm install @supabase/supabase-js
npm install react-router-dom
npm install recharts
npm install lucide-react
npm install axios

# Install TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Configure TailwindCSS**:

Edit `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Edit `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**Verification**:
```powershell
npm run dev
# Should start on http://localhost:5173
```

- [ ] Vite project created
- [ ] All packages installed
- [ ] TailwindCSS configured
- [ ] Dev server runs successfully

---

### Step 9: Create Frontend Folder Structure (20 minutes)

```powershell
# Navigate to src directory
cd src

# Create directories
mkdir components
mkdir pages
mkdir services
mkdir hooks
mkdir types
mkdir utils

# Create .gitkeep files to preserve empty directories
New-Item -Path components\.gitkeep -ItemType File
New-Item -Path pages\.gitkeep -ItemType File
New-Item -Path hooks\.gitkeep -ItemType File
New-Item -Path types\.gitkeep -ItemType File
New-Item -Path utils\.gitkeep -ItemType File
```

**Verification**:
- [ ] All folders created
- [ ] .gitkeep files added

---

### Step 10: Create Frontend Configuration Files (30 minutes)

**File 1: `.env.example`**

Create `b:\Project\SaaS\Second\lead-automation-frontend\.env.example`:

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here

# Backend API
VITE_API_URL=http://localhost:8000
```

**File 2: `.env`**

Create `b:\Project\SaaS\Second\lead-automation-frontend\.env`:

```env
# Supabase Configuration
VITE_SUPABASE_URL=<PASTE_YOUR_SUPABASE_URL>
VITE_SUPABASE_ANON_KEY=<PASTE_YOUR_ANON_KEY>

# Backend API
VITE_API_URL=http://localhost:8000
```

**File 3: `.gitignore`** (Update existing)

Ensure these lines are in `.gitignore`:

```gitignore
# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules

# Build
dist
dist-ssr
*.local

# Editor
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

**File 4: `src/services/supabase.ts`**

Create `b:\Project\SaaS\Second\lead-automation-frontend\src\services\supabase.ts`:

```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

**File 5: `src/services/api.ts`**

Create `b:\Project\SaaS\Second\lead-automation-frontend\src\services\api.ts`:

```typescript
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Health check function
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}
```

**Verification**:
```powershell
# Test if services can be imported (compile check)
npm run build
# Should build without errors
```

- [ ] All config files created
- [ ] Environment variables set
- [ ] Service files created
- [ ] Build succeeds

---

### Step 11: Update App.tsx with Test UI (20 minutes)

**File: `src/App.tsx`**

Replace content with:

```typescript
import { useState, useEffect } from 'react'
import { checkHealth } from './services/api'
import './App.css'

function App() {
  const [healthStatus, setHealthStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkHealth()
        setHealthStatus(data)
        setError(null)
      } catch (err) {
        setError('Failed to connect to backend API')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchHealth()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Lead Automation System
        </h1>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Backend Health Check
          </h2>
          
          {loading && (
            <p className="text-gray-600">Checking backend connection...</p>
          )}
          
          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-4">
              <p className="text-red-800">{error}</p>
              <p className="text-sm text-red-600 mt-2">
                Make sure backend is running on http://localhost:8000
              </p>
            </div>
          )}
          
          {healthStatus && (
            <div className="bg-green-50 border border-green-200 rounded p-4">
              <p className="text-green-800 font-semibold mb-2">
                ✅ Backend Connected!
              </p>
              <div className="text-sm text-gray-700">
                <p><strong>Status:</strong> {healthStatus.status}</p>
                <p className="mt-2"><strong>Services:</strong></p>
                <ul className="ml-4 mt-1">
                  {Object.entries(healthStatus.services || {}).map(([key, value]) => (
                    <li key={key}>
                      {key}: <span className="font-medium">{value as string}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
        
        <div className="text-sm text-gray-600">
          <p><strong>Phase 2:</strong> Infrastructure Setup ✅</p>
          <p className="mt-1"><strong>Next:</strong> Phase 3 - Database Schema</p>
        </div>
      </div>
    </div>
  )
}

export default App
```

**Verification**:
```powershell
# Start frontend (in frontend directory)
npm run dev

# Start backend (in backend directory, separate terminal)
cd b:\Project\SaaS\Second\lead-automation-backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

- [ ] Frontend shows UI at http://localhost:5173
- [ ] Backend connection status displayed
- [ ] Green success message if backend is running
- [ ] TailwindCSS styles applied correctly

---

### Step 12: Create Frontend README (15 minutes)

**File: `README.md`**

Create `b:\Project\SaaS\Second\lead-automation-frontend\README.md`:

```markdown
# Lead Automation Frontend

React + TypeScript frontend for AI-powered lead management system.

## Tech Stack

- **Framework**: React 18 + Vite
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **State**: React Hooks
- **Routing**: React Router DOM
- **Charts**: Recharts
- **Icons**: Lucide React
- **API Client**: Axios
- **Database**: Supabase (client library)

## Setup

### 1. Install Dependencies

```powershell
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```powershell
cp .env.example .env
```

Required environment variables:
- VITE_SUPABASE_URL
- VITE_SUPABASE_ANON_KEY
- VITE_API_URL

### 3. Run Development Server

```powershell
npm run dev
```

Application will be available at: http://localhost:5173

## Build

```powershell
npm run build
```

Built files will be in `dist/` directory.

## Project Structure

```
src/
├── components/      # Reusable React components
├── pages/          # Page components
├── services/       # API clients (backend, Supabase)
├── hooks/          # Custom React hooks
├── types/          # TypeScript type definitions
├── utils/          # Utility functions
├── App.tsx         # Main app component
└── main.tsx        # Entry point
```

## Development

- Phase 2: Infrastructure setup ✅
- Phase 3: Database schema (next)
- Phase 5: UI components
- Phase 6: Integration
```

**Verification**:
- [ ] README.md created with setup instructions

---

### Step 13: Initialize Git Repositories (30 minutes)

**Backend Git Setup**:

```powershell
cd b:\Project\SaaS\Second\lead-automation-backend

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Backend infrastructure setup (Phase 2)"

# Optional: Connect to remote repository
# git remote add origin <your-backend-repo-url>
# git push -u origin main
```

**Frontend Git Setup**:

```powershell
cd b:\Project\SaaS\Second\lead-automation-frontend

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Frontend infrastructure setup (Phase 2)"

# Optional: Connect to remote repository
# git remote add origin <your-frontend-repo-url>
# git push -u origin main
```

**Verification**:
```powershell
# Check git status
git status
# Should show: "nothing to commit, working tree clean"

# View commit
git log --oneline
```

- [ ] Backend git initialized
- [ ] Frontend git initialized
- [ ] Initial commits created
- [ ] .gitignore working (.env not tracked)

---

## ✅ Phase 2 Completion Checklist

### External Services
- [ ] Supabase project created
- [ ] Supabase API keys obtained
- [ ] Groq API account created
- [ ] Groq API key obtained
- [ ] Resend email account created
- [ ] Resend API key obtained

### Backend
- [ ] Python virtual environment created
- [ ] All dependencies installed (requirements.txt)
- [ ] Project folder structure created
- [ ] .env file configured with API keys
- [ ] config.py loads settings correctly
- [ ] main.py FastAPI app created
- [ ] Health check endpoints working
- [ ] Server runs on http://localhost:8000
- [ ] Swagger docs accessible at /docs
- [ ] README.md created
- [ ] Git repository initialized
- [ ] .gitignore configured

### Frontend
- [ ] Vite React TypeScript project created
- [ ] All npm packages installed
- [ ] TailwindCSS configured
- [ ] Project folder structure created
- [ ] .env file configured
- [ ] Supabase client created (services/supabase.ts)
- [ ] API client created (services/api.ts)
- [ ] App.tsx updated with health check UI
- [ ] Dev server runs on http://localhost:5173
- [ ] Backend connection test works
- [ ] README.md created
- [ ] Git repository initialized
- [ ] .gitignore configured

### Integration Test
- [ ] Backend server running without errors
- [ ] Frontend server running without errors
- [ ] Frontend can connect to backend API
- [ ] Health check shows green status
- [ ] No CORS errors in browser console

---

## 🎯 Success Metrics

| Metric | Target | Verification Method |
|--------|--------|---------------------|
| **Backend Server Startup** | < 5 seconds | Time from command to "Uvicorn running" |
| **Frontend Build** | No TypeScript errors | `npm run build` succeeds |
| **API Response Time** | < 100ms | /health endpoint response |
| **Dependencies Installed** | 100% success rate | No pip/npm errors |
| **Environment Variables** | All required vars set | Config loads without errors |
| **Git Repository** | Clean working tree | `git status` shows clean |
| **Documentation** | README in both projects | Files exist and complete |

---

## 🚨 Common Issues & Solutions

### Issue 1: Python Virtual Environment Won't Activate

**Symptom**: `.\venv\Scripts\Activate.ps1` gives execution policy error

**Solution**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### Issue 2: Port Already in Use

**Symptom**: "Address already in use" error on port 8000 or 5173

**Solution**:
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <process_id> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

### Issue 3: Supabase Connection Failed

**Symptom**: Backend can't connect to Supabase

**Solution**:
- Verify SUPABASE_URL and keys in .env
- Check Supabase project is active (not paused)
- Test connection with:
```python
from supabase import create_client
client = create_client(url, key)
print(client)  # Should not error
```

---

### Issue 4: CORS Error in Browser

**Symptom**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**:
- Verify `CORS_ORIGINS` in backend .env includes `http://localhost:5173`
- Restart backend server after changing .env
- Check CORSMiddleware is configured in main.py

---

### Issue 5: TailwindCSS Not Working

**Symptom**: Styles not applied, classes like `bg-gray-50` have no effect

**Solution**:
- Verify `tailwind.config.js` has correct content paths
- Verify `@tailwind` directives in `src/index.css`
- Restart dev server
- Clear browser cache

---

### Issue 6: Module Not Found Errors

**Backend**: 
```powershell
# Ensure venv is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Frontend**:
```powershell
# Delete node_modules and reinstall
rm -r node_modules
rm package-lock.json
npm install
```

---

## 📦 Deliverables Summary

### Phase 2 Outputs

**External Accounts**:
1. Supabase project with database
2. Groq API account with key
3. Resend email account with key

**Backend Application**:
4. Complete FastAPI project structure
5. Working health check API
6. Environment configuration system
7. README documentation
8. Git repository with initial commit

**Frontend Application**:
9. Complete React + Vite project structure
10. Working dev server with test UI
11. API client services configured
12. README documentation
13. Git repository with initial commit

### Handoff to Phase 3

**Required for Next Phase**:
- [ ] Supabase project URL and keys
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Both projects tracked in Git

**Inputs for Phase 3**:
- Supabase credentials → Database schema creation
- Backend utils/db.py → Supabase client implementation
- Frontend services/supabase.ts → Database queries

---

## 📅 Daily Schedule (Detailed)

### Day 2: Backend Setup (6-7 hours)

**Morning Session (9 AM - 12 PM)**
- 9:00-9:30: Create Supabase project
- 9:30-9:45: Create Groq API account
- 9:45-10:00: Create Resend email account
- 10:00-10:45: Initialize backend project, create venv, install dependencies
- 10:45-11:15: Create configuration files (.env, config.py)
- 11:15-12:00: Create main.py FastAPI application

**Afternoon Session (1 PM - 5 PM)**
- 1:00-1:30: Test backend server, verify health endpoints
- 1:30-2:00: Create README.md
- 2:00-2:30: Initialize Git repository
- 2:30-3:30: **Buffer time** for troubleshooting issues
- 3:30-4:00: Document any deviations or issues
- 4:00-5:00: **Optional**: Start frontend setup early

**End of Day Deliverables**:
- Backend server running ✅
- All external API keys obtained ✅
- Git repository initialized ✅

---

### Day 3: Frontend Setup (5-6 hours)

**Morning Session (9 AM - 12 PM)**
- 9:00-9:45: Initialize Vite React TypeScript project
- 9:45-10:15: Install all npm dependencies
- 10:15-10:45: Configure TailwindCSS
- 10:45-11:20: Create folder structure
- 11:20-12:00: Create configuration files (.env, services)

**Afternoon Session (1 PM - 5 PM)**
- 1:00-1:30: Update App.tsx with health check UI
- 1:30-2:00: Test frontend-backend connection
- 2:00-2:30: Create README.md
- 2:30-3:00: Initialize Git repository
- 3:00-4:00: **Integration testing** (both servers running)
- 4:00-5:00: **Final verification** using completion checklist

**End of Day Deliverables**:
- Frontend server running ✅
- Backend connection successful ✅
- Phase 2 complete and ready for Phase 3 ✅

---

## 🎓 Learning Outcomes

By completing Phase 2, you will:

1. **Environment Setup Mastery**: Configure Python venv and Node.js projects
2. **Configuration Management**: Securely handle API keys and environment variables
3. **FastAPI Basics**: Create basic API with health check endpoints
4. **React + Vite**: Initialize modern React project with TypeScript
5. **TailwindCSS**: Configure utility-first CSS framework
6. **API Integration**: Connect frontend to backend REST API
7. **Version Control**: Initialize Git repositories with proper .gitignore
8. **Documentation**: Write clear setup instructions

---

## 📚 Reference Materials

### Official Documentation
- **FastAPI**: https://fastapi.tiangolo.com
- **Vite**: https://vitejs.dev
- **React**: https://react.dev
- **TailwindCSS**: https://tailwindcss.com
- **Supabase**: https://supabase.com/docs
- **Groq**: https://console.groq.com/docs
- **Resend**: https://resend.com/docs

### Internal Documents
- `PROJECT_IMPLEMENTATION_PLAN.md` - Overall project plan
- `Phase_1_.md` - Previous phase (documentation)
- `.env.example` - Environment variable template

---

## 🔄 Iteration Plan

Phase 2 is infrastructure-focused. Minimal iteration expected, but:

**If issues arise**:
1. Document the issue in GitHub Issues (or notepad)
2. Try troubleshooting steps from "Common Issues" section
3. Search official documentation
4. If blocked >2 hours, consider alternative approach
5. Update this document with solution for future reference

**Key principle**: Don't over-engineer. Get it working, then optimize later.

---

## ✨ Phase 2 Completion Criteria

**Definition of Done**:
- [ ] All external service accounts created
- [ ] Backend project initialized and running
- [ ] Frontend project initialized and running
- [ ] Health check API working
- [ ] Frontend can connect to backend
- [ ] All environment variables configured
- [ ] Git repositories initialized for both projects
- [ ] README.md documentation complete
- [ ] No errors in console (backend or frontend)
- [ ] Completion checklist 100% checked

**When to proceed to Phase 3**:
✅ All checkboxes above completed  
✅ Both dev servers running simultaneously without errors  
✅ Integration test passed (frontend shows green backend status)  

---

## 📞 Support & Escalation

**If you get stuck**:

1. **Dependency Issues**: Check official package documentation, try different version
2. **API Key Issues**: Verify keys are copied correctly, check service status pages
3. **Port Conflicts**: Use different ports, kill conflicting processes
4. **CORS Issues**: Double-check CORS_ORIGINS configuration

**Escalation Path**:
- <1 hour blocked → Google error, check Stack Overflow
- 1-2 hours blocked → Try alternative approach
- >2 hours blocked → Document issue, consider moving to Phase 3 (some issues can be resolved later)

---

## 🏆 Success Indicators

**You've succeeded in Phase 2 when**:

✅ You can run `uvicorn app.main:app --reload` and see: "Uvicorn running"  
✅ You can visit http://localhost:8000/docs and see Swagger UI  
✅ You can run `npm run dev` and see: "Local: http://localhost:5173"  
✅ Frontend UI shows green "Backend Connected!" message  
✅ No red errors in terminal or browser console  
✅ You understand where each API key is used  
✅ You can explain the project structure to someone else  

---

**🚀 Infrastructure Ready - Let's Build Features!**

---

**Document Metadata**:
- **Phase**: 2 of 9
- **Duration**: 2 days (Day 2-3)
- **Dependencies**: Phase 1 complete
- **Output Type**: Infrastructure & Configuration
- **Team Size**: 1 person
- **Skills Required**: Python, Node.js, environment setup, basic terminal commands
- **Next Phase**: Phase 3 - Database Schema & Models

---

*This master plan is a living document. Update it as you encounter new issues and solutions.*
