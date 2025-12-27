from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="""
    ## AI-Powered Lead Management Automation System
    
    ### Features
    * 🤖 **Automated Lead Capture** - AI categorization with Groq
    * 📧 **Email Automation** - Acknowledgement emails via Resend
    * ⏱️ **SLA Tracking** - Automated assignment and deadline enforcement
    * 📊 **Real-time Analytics** - Dashboard stats and conversion metrics
    * ✅ **Approval Workflows** - Human-in-the-loop for high-value leads
    * 📅 **Follow-up Scheduling** - Automated task creation
    
    ### Workflow
    1. Lead submits form → Stored in database
    2. AI categorizes lead (priority, intent, suggested action)
    3. Auto-assignment with SLA deadline
    4. Acknowledgement email sent
    5. Follow-up tasks created for high-priority leads
    
    ### API Endpoints
    - **Leads**: Create, list, update, recategorize
    - **Analytics**: Dashboard, conversion funnel, SLA performance
    - **Follow-ups**: List pending, complete, snooze
    - **Approvals**: List pending, approve, reject
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
from app.api import leads, analytics, approvals, follow_ups
app.include_router(leads.router)
app.include_router(analytics.router)
app.include_router(approvals.router)
app.include_router(follow_ups.router)


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
    """
    Detailed health check endpoint
    
    Tests all critical services:
    - Database connection (Supabase)
    - AI service (Groq)
    - Email service (Resend)
    
    Returns:
    - status: overall system health
    - services: individual service statuses
    - database_stats: real-time metrics
    """
    from app.utils.db import get_dashboard_stats
    from app.services.ai_service import get_ai_service
    from app.services.email_service import get_email_service
    
    # Test database connection
    db_status = "operational"
    db_stats = None
    try:
        db_stats = await get_dashboard_stats()
        db_connected = True
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_connected = False
    
    # Test AI service
    ai_status = "operational"
    try:
        ai = get_ai_service()
        if ai.client is None:
            ai_status = "not_configured"
    except Exception as e:
        ai_status = f"error: {str(e)}"
    
    # Test Email service
    email_status = "operational"
    try:
        email = get_email_service()
        if not email.from_email:
            email_status = "not_configured"
    except Exception as e:
        email_status = f"error: {str(e)}"
    
    # Determine overall status
    all_operational = (
        db_connected and 
        ai_status == "operational" and 
        email_status == "operational"
    )
    
    return {
        "status": "healthy" if all_operational else "degraded",
        "services": {
            "api": "operational",
            "database": db_status,
            "supabase": "operational" if db_connected else "error",
            "groq": ai_status,
            "resend": email_status
        },
        "database_stats": db_stats if db_connected else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Auto-reload on code changes
    )
