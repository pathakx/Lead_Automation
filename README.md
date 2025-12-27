# 🚀 AI-Powered Lead Management & Automation System

> **Intelligent lead capture, categorization, and follow-up automation for modern sales teams**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?style=flat&logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Lead Automation System** is a complete lead management solution that combines AI-powered categorization, automated workflows, and intelligent follow-up scheduling to help sales teams convert leads faster.

### 🎬 What It Does

1. **Captures** leads from web forms
2. **Analyzes** them using AI (Groq LLM)
3. **Categorizes** by priority, intent, and suggested action
4. **Sends** automated acknowledgment emails
5. **Creates** follow-up tasks based on priority
6. **Tracks** SLA compliance and conversion metrics
7. **Manages** approval workflows for high-value leads

### 💡 Perfect For

- **Sales Teams** - Automate lead qualification and follow-ups
- **Marketing Agencies** - Track and nurture leads efficiently
- **SaaS Companies** - Manage product trials and demo requests
- **B2B Businesses** - Handle bulk inquiries and quotes

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Smart Categorization** - Groq LLM analyzes lead intent, priority, and suggests actions
- **Dynamic Prioritization** - High/Medium/Low priority auto-assignment
- **Intent Recognition** - Identifies purchase intent, research, or support needs

### 📧 Email Automation
- **Instant Acknowledgment** - Automated emails via Resend API
- **Personalized Templates** - Dynamic content based on products of interest
- **Delivery Tracking** - Email status monitoring

### ✅ Approval Workflows
- **Human-in-the-Loop** - Approvals for high-value scenarios
- **Smart Triggers**:
  - Large quantity orders (100+ units)
  - High-priority professionals (Architects, Builders)
  - Bulk discount requests
- **Complete Audit Trail** - Track approval history

### 📅 Follow-Up Management
- **Automated Scheduling**:
  - High Priority → 30-minute call
  - Medium Priority → 24-hour email
  - Low Priority → 3-day nurture
- **Snooze & Complete** - Flexible task management
- **Priority Filtering** - Focus on what matters

### 📊 Analytics Dashboard
- **Real-time Metrics**:
  - Total leads, conversion rate, response time
  - Priority distribution
  - Conversion funnel
  - SLA compliance tracking
- **Visual Charts** - Recharts integration

### ⏱️ SLA Tracking
- **Automated Deadlines** - Based on lead priority
- **Compliance Monitoring** - Track on-time responses
- **Performance Metrics** - Team efficiency insights

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **AI/LLM**: Groq (Llama 3.3 70B)
- **Database**: Supabase (PostgreSQL)
- **Email**: Resend API
- **Authentication**: JWT (ready for implementation)

### Frontend
- **Framework**: React 19.2 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router v7
- **HTTP Client**: Axios

### DevOps & Tools
- **Version Control**: Git
- **Package Managers**: pip, npm
- **Development**: Hot reload (Vite, Uvicorn)
- **Testing**: Pytest (backend)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│                    (Web Form Submission)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Lead Service │  │  AI Service  │  │ Email Service│      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────┐       │
│  │           Supabase PostgreSQL Database            │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   REACT FRONTEND                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Follow-ups│  │Approvals │  │Analytics │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Lead Submission** → FastAPI endpoint
2. **AI Analysis** → Groq categorizes lead
3. **Database Storage** → Supabase PostgreSQL
4. **Email Dispatch** → Resend sends acknowledgment
5. **Task Creation** → Follow-up scheduled
6. **Admin Dashboard** → Real-time updates

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Node.js 18+** and npm
- **Supabase Account** (free tier works)
- **Groq API Key** (free tier: 30 req/min)
- **Resend API Key** (free tier: 100 emails/day)

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/lead-automation-system.git
cd lead-automation-system
```

### 2️⃣ Backend Setup

```bash
cd lead-automation-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Frontend Setup

```bash
cd lead-automation-frontend

# Install dependencies
npm install
```

---

## ⚙️ Configuration

### Backend Environment Variables

Create `.env` file in `lead-automation-backend/`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Groq AI Configuration
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile

# Resend Email Configuration
RESEND_API_KEY=your-resend-api-key-here
RESEND_FROM_EMAIL=onboarding@resend.dev

# Application Settings
APP_NAME=Lead Automation API
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Environment Variables

Create `.env` file in `lead-automation-frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### Database Setup

1. **Create Supabase Project** at [supabase.com](https://supabase.com)
2. **Run the schema** (provided in `/database_schema.sql`)
3. **Copy API keys** to `.env` files

---

## 🎮 Usage

### Start Backend Server

```bash
cd lead-automation-backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**
- API Docs: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### Start Frontend Dev Server

```bash
cd lead-automation-frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### Access the Application

1. **Admin Dashboard**: http://localhost:5173
2. **API Documentation**: http://localhost:8000/docs

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 📧 Leads
```http
POST   /api/leads/              # Create new lead
GET    /api/leads/              # List all leads
PUT    /api/leads/{id}          # Update lead
POST   /api/leads/{id}/recategorize  # Re-run AI categorization
```

#### 📊 Analytics
```http
GET    /api/analytics/dashboard          # Dashboard stats
GET    /api/analytics/conversion         # Conversion funnel
GET    /api/analytics/sla-performance    # SLA metrics
```

#### ✅ Follow-ups
```http
GET    /api/follow-ups/pending    # List pending follow-ups
GET    /api/follow-ups/completed  # List completed
GET    /api/follow-ups/snoozed    # List snoozed
GET    /api/follow-ups/stats      # Follow-up statistics
POST   /api/follow-ups/{id}/complete  # Mark complete
POST   /api/follow-ups/{id}/snooze    # Snooze task
```

#### 🔐 Approvals
```http
GET    /api/approvals/pending     # List pending approvals
GET    /api/approvals/approved    # Approval history
GET    /api/approvals/rejected    # Rejection history
GET    /api/approvals/stats       # Approval statistics
POST   /api/approvals/{id}/approve  # Approve request
POST   /api/approvals/{id}/reject   # Reject request
```

**Full API documentation available at `/docs` endpoint**

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=Analytics+Dashboard)

### Follow-ups Management
![Follow-ups](https://via.placeholder.com/800x400/059669/FFFFFF?text=Follow-up+Queue)

### Approval Workflows
![Approvals](https://via.placeholder.com/800x400/DC2626/FFFFFF?text=Approval+Management)

---

## 🗂️ Project Structure

```
lead-automation-system/
├── lead-automation-backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── leads.py
│   │   │   ├── analytics.py
│   │   │   ├── follow_ups.py
│   │   │   └── approvals.py
│   │   ├── services/         # Business logic
│   │   │   ├── lead_service.py
│   │   │   ├── ai_service.py
│   │   │   └── email_service.py
│   │   ├── utils/            # Utilities
│   │   │   └── db.py
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── .env
│
├── lead-automation-frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── FollowUpQueue.tsx
│   │   │   ├── ApprovalQueue.tsx
│   │   │   └── Analytics.tsx
│   │   ├── services/         # API services
│   │   │   └── api.ts
│   │   ├── utils/            # Utilities
│   │   │   └── dateUtils.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env
│
├── database_schema.sql
└── README.md
```

---

## 🧪 Testing

### Backend Tests
```bash
cd lead-automation-backend
pytest
```

### Frontend Build
```bash
cd lead-automation-frontend
npm run build
```

---

## 🚢 Deployment

### Backend (FastAPI)

**Recommended platforms**:
- **Railway** / **Render** - Free tier available
- **AWS EC2** / **DigitalOcean** - More control
- **Docker** - Containerized deployment

```bash
# Build and run via Docker
docker build -t lead-automation-backend .
docker run -p 8000:8000 lead-automation-backend
```

### Frontend (React)

**Recommended platforms**:
- **Vercel** - Zero-config deployment
- **Netlify** - Auto-deploy from Git
- **Cloudflare Pages** - Fast global CDN

```bash
# Build production bundle
npm run build

# Deploy dist/ folder to your platform
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Coding Standards
- **Backend**: Follow PEP 8 (Python)
- **Frontend**: Use TypeScript with ESLint
- **Commits**: Use conventional commit messages

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** - Fast LLM inference
- **Supabase** - Backend-as-a-Service
- **Resend** - Email delivery
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Tailwind CSS** - Utility-first CSS

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/lead-automation-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lead-automation-system/discussions)
- **Email**: support@yourcompany.com

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

## 📈 Roadmap

### Upcoming Features
- [ ] Multi-tenant support
- [ ] WhatsApp integration
- [ ] Advanced analytics & reporting
- [ ] Email template builder
- [ ] Role-based access control
- [ ] Mobile app (React Native)
- [ ] Webhook integrations
- [ ] CRM integrations (Salesforce, HubSpot)

---

**Built with ❤️ for modern sales teams**

*Last Updated: December 2024*
