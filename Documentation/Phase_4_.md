# Phase 4: Backend Development - Master Plan
## AI-Powered Lead Management Automation System

---

## 📅 Timeline: Days 4-8
**Status**: 🚀 Ready for Implementation  
**Last Updated**: December 27, 2024  
**Prerequisites**: Phase 3 completed (Database schema, models, and utilities ready)

---

## 🎯 Phase 4 Objectives

### Primary Goal
Implement the complete FastAPI backend with all API endpoints, integrate AI service (Groq) for lead categorization, integrate email service (Resend) for automated communications, and establish business logic layer for lead automation workflows.

### Success Criteria
- ✅ All API endpoints implemented and functional
- ✅ AI categorization service integrated with Gro

q
- ✅ Email service integrated with Resend
- ✅ Lead capture workflow end-to-end working
- ✅ Automated lead assignment implemented
- ✅ SLA tracking functional
- ✅ Follow-up scheduling working
- ✅ Approval workflow implemented
- ✅ Analytics endpoints returning data

---

## 📋 Deliverables

### 1. API Layer
- ✅ Lead endpoints (CRUD + categorization)
- ✅ Product endpoints
- ✅ Activity endpoints
- ✅ Assignment endpoints
- ✅ Follow-up endpoints
- ✅ Approval endpoints
- ✅ Analytics endpoints
- ✅ Admin endpoints

### 2. Service Layer
- ✅ AI Service (Groq integration)
- ✅ Email Service (Resend integration)
- ✅ Lead Service (business logic)
- ✅ Scheduler Service (background tasks)

### 3. Business Logic
- ✅ Lead capture automation workflow
- ✅ Auto-assignment rules
- ✅ SLA enforcement
- ✅ Approval triggers
- ✅ Follow-up scheduling

### 4. Testing & Verification
- ✅ API endpoint tests
- ✅ AI service tests
- ✅ Email service tests
- ✅ End-to-end workflow tests

---

## 📝 Detailed Implementation Steps

## DAY 4-5: Service Layer Implementation

### Step 1: Create AI Service (Groq Integration) (60 minutes)

**Objective**: Implement production-ready AI service for lead categorization with retry logic and fallback

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\services\ai_service.py`

**Implementation**:

```python
from groq import Groq
from typing import Dict, Any, Optional
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AIService:
    """
    Production-ready AI service with:
    - Versioning for auditability
    - Fallback categorization
    - Retry logic
    - Error handling
    """
    
    MODEL_VERSION = "llama-3.1-70b-versatile"
    PROMPT_VERSION = "v1.0"  # Increment when changing prompts
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    async def categorize_lead(
        self, 
        lead_data: Dict[str, Any],
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """
        Categorize lead using AI with fallback
        
        Returns dict with:
        - input: original lead data (for replay)
        - output: AI categorization
        - model: model version used
        - prompt_version: prompt version used
        - method: 'ai' or 'fallback'
        - timestamp: when categorization happened
        """
        
        # Store original input for replay capability
        lead_input = {
            "role": lead_data.get('role'),
            "location": lead_data.get('location'),
            "products": lead_data.get('products', []),
            "message": lead_data.get('message')
        }
        
        # Try AI categorization with retries
        for attempt in range(retry_count):
            try:
                result = await self._call_groq_api(lead_input)
                
                return {
                    "input": lead_input,
                    "output": result,
                    "model": self.MODEL_VERSION,
                    "prompt_version": self.PROMPT_VERSION,
                    "method": "ai",
                    "timestamp": datetime.utcnow().isoformat(),
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                logger.warning(f"AI categorization attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    continue  # Retry
                else:
                    # All retries failed, use fallback
                    logger.error(f"All AI attempts failed, using fallback for lead")
                    return self.fallback_categorization(lead_input)
    
    async def _call_groq_api(self, lead_input: Dict) -> Dict:
        """Make actual Groq API call"""
        
        prompt = f"""
        Analyze this lead inquiry and categorize it:
        
        Role: {lead_input.get('role')}
        Location: {lead_input.get('location')}
        Products: {', '.join(lead_input.get('products', []))}
        Message: {lead_input.get('message')}
        
        Provide categorization in JSON format:
        {{
          "intent": "quote_request" | "product_info" | "support" | "complaint" | "other",
          "lead_type": "home_owner" | "architect" | "builder" | "contractor",
          "priority": "high" | "medium" | "low",
          "suggested_action": "call_within_30_min" | "email_response" | "schedule_demo" | "nurture",
          "reasoning": "brief explanation"
        }}
        
        Respond ONLY with valid JSON.
        """
        
        response = self.client.chat.completions.create(
            model=self.MODEL_VERSION,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
            timeout=30  # 30 second timeout
        )
        
        return json.loads(response.choices[0].message.content)
    
    def fallback_categorization(self, lead_input: Dict) -> Dict:
        """
        Simple rule-based fallback when AI fails
        Uses keyword matching and heuristics
        """
        
        message = (lead_input.get('message') or '').lower()
        role = (lead_input.get('role') or '').lower()
        
        # Determine priority based on keywords
        urgent_keywords = ["urgent", "asap", "immediately", "need now", "today"]
        quote_keywords = ["quote", "price", "cost", "budget", "estimate"]
        
        is_urgent = any(kw in message for kw in urgent_keywords)
        wants_quote = any(kw in message for kw in quote_keywords)
        
        if is_urgent or wants_quote:
            priority = "high"
            suggested_action = "call_within_30_min"
            intent = "quote_request"
        else:
            priority = "medium"
            suggested_action = "email_response"
            intent = "product_info"
        
        # Map role to lead_type
        lead_type_map = {
            "home owner": "home_owner",
            "architect": "architect",
            "builder": "builder",
            "contractor": "contractor"
        }
        lead_type = lead_type_map.get(role, "home_owner")
        
        return {
            "input": lead_input,
            "output": {
                "intent": intent,
                "lead_type": lead_type,
                "priority": priority,
                "suggested_action": suggested_action,
                "reasoning": "Fallback rule-based categorization (AI unavailable)"
            },
            "model": "rule_based_fallback",
            "prompt_version": "N/A",
            "method": "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }


# Initialize AI service (singleton)
ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        from app.config import settings
        ai_service = AIService(api_key=settings.GROQ_API_KEY)
    return ai_service
```

**Dependencies to Install**:
```bash
pip install groq
```

**Verification**:
```python
# Test script
from app.services.ai_service import get_ai_service
import asyncio

async def test_ai():
    ai = get_ai_service()
    result = await ai.categorize_lead({
        "role": "Architect",
        "location": "Mumbai",
        "products": ["Flooring", "Wall Panels"],
        "message": "Need urgent quote for luxury apartment project"
    })
    print("AI Result:", result)

asyncio.run(test_ai())
```

- [ ] AI service file created
- [ ] Groq package installed
- [ ] Test categorization successful
- [ ] Fallback logic tested

---

### Step 2: Create Email Service (Resend Integration) (45 minutes)

**Objective**: Implement email service for sending automated emails

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\services\email_service.py`

**Implementation**:

```python
import resend
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Email service using Resend API"""
    
    def __init__(self, api_key: str, from_email: str):
        resend.api_key = api_key
        self.from_email = from_email
    
    async def send_acknowledgement(
        self,
        to_email: str,
        name: str,
        products: List[str]
    ) -> Dict[str, Any]:
        """Send acknowledgement email to new lead"""
        
        subject = f"Thank you for your inquiry, {name}!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Thank you for contacting us!</h2>
            <p>Dear {name},</p>
            <p>We've received your inquiry about:</p>
            <ul>
                {"".join([f"<li>{product}</li>" for product in products])}
            </ul>
            <p>Our team will review your request and get back to you within 24 hours.</p>
            <p>Best regards,<br>The Sales Team</p>
        </body>
        </html>
        """
        
        try:
            result = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })
            
            logger.info(f"Acknowledgement email sent to {to_email}, ID: {result['id']}")
            
            return {
                "success": True,
                "resend_id": result['id'],
                "template": "acknowledgement",
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send acknowledgement email to {to_email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "template": "acknowledgement"
            }
    
    async def send_custom_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> Dict[str, Any]:
        """Send custom email"""
        
        try:
            result = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })
            
            return {
                "success": True,
                "resend_id": result['id'],
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Initialize email service (singleton)
email_service = None

def get_email_service() -> EmailService:
    """Get or create email service instance"""
    global email_service
    if email_service is None:
        from app.config import settings
        email_service = EmailService(
            api_key=settings.RESEND_API_KEY,
            from_email=settings.RESEND_FROM_EMAIL
        )
    return email_service
```

**Dependencies to Install**:
```bash
pip install resend
```

**Verification**:
```python
# Test email
from app.services.email_service import get_email_service
import asyncio

async def test_email():
    email = get_email_service()
    result = await email.send_acknowledgement(
        to_email="test@example.com",
        name="Test User",
        products=["Flooring", "Wall Panels"]
    )
    print("Email Result:", result)

asyncio.run(test_email())
```

- [ ] Email service file created
- [ ] Resend package installed
- [ ] Test email sent successfully

---

### Step 3: Create Lead Service (Business Logic) (90 minutes)

**Objective**: Implement business logic for lead processing workflow

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\services\lead_service.py`

**Implementation**:

```python
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
from app.utils.db import (
    insert_record,
    update_record,
    get_record,
    query_records
)
from app.services.ai_service import get_ai_service
from app.services.email_service import get_email_service

logger = logging.getLogger(__name__)

class LeadService:
    """Business logic for lead processing"""
    
    def __init__(self):
        self.ai_service = get_ai_service()
        self.email_service = get_email_service()
    
    async def create_lead_with_products(
        self,
        lead_data: Dict[str, Any],
        product_interests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Complete lead capture workflow:
        1. Insert lead
        2. Insert products
        3. AI categorization
        4. Log AI activity
        5. Auto-assign
        6. Send acknowledgement email
        7. Create follow-up
        """
        
        # Step 1: Insert lead
        lead = await insert_record("leads", {
            "name": lead_data["name"],
            "email": lead_data["email"],
            "phone": lead_data.get("phone"),
            "company": lead_data.get("company"),
            "role": lead_data.get("role"),
            "location": lead_data.get("location"),
            "message": lead_data.get("message"),
            "source": lead_data.get("source", "website_form"),
            "status": "new"
        })
        
        lead_id = lead["id"]
        logger.info(f"Created lead {lead_id}")
        
        # Step 2: Insert products
        products = []
        for product in product_interests:
            p = await insert_record("lead_products", {
                "lead_id": lead_id,
                "category": product["category"],
                "product": product["product"],
                "quantity": product.get("quantity"),
                "notes": product.get("notes")
            })
            products.append(p)
        
        # Step 3: AI Categorization
        ai_result = await self.ai_service.categorize_lead({
            "role": lead_data.get("role"),
            "location": lead_data.get("location"),
            "products": [p["product"] for p in product_interests],
            "message": lead_data.get("message")
        })
        
        # Step 4: Log AI activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "ai_result",
            "status": "completed",
            "message": "AI analyzed lead and suggested priority action",
            "actor_type": "ai",
            "metadata": ai_result
        })
        
        # Step 5: Auto-assign based on priority
        priority = ai_result["output"]["priority"]
        sla_hours = 1 if priority == "high" else 24
        
        assignment = await insert_record("assignments", {
            "lead_id": lead_id,
            "owner_id": "system_auto",  # TODO: Implement round-robin assignment
            "owner_name": "Auto-assigned",
            "sla_deadline": (datetime.utcnow() + timedelta(hours=sla_hours)).isoformat()
        })
        
        # Log assignment activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "assignment",
            "status": "completed",
            "message": f"Lead auto-assigned with {sla_hours}h SLA",
            "actor_type": "system",
            "metadata": {
                "owner_id": assignment["owner_id"],
                "sla_deadline": assignment["sla_deadline"]
            }
        })
        
        # Step 6: Send acknowledgement email
        email_result = await self.email_service.send_acknowledgement(
            to_email=lead_data["email"],
            name=lead_data["name"],
            products=[p["product"] for p in product_interests]
        )
        
        # Log email activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "email",
            "status": "completed" if email_result["success"] else "failed",
            "message": "Acknowledgement email sent" if email_result["success"] else "Email failed",
            "actor_type": "system",
            "metadata": email_result
        })
        
        # Update first_response_at
        if email_result["success"]:
            await update_record("leads", lead_id, {
                "first_response_at": datetime.utcnow().isoformat()
            })
        
        # Step 7: Create follow-up if high priority
        if priority == "high":
            await insert_record("lead_activity", {
                "lead_id": lead_id,
                "type": "follow_up",
                "status": "pending",
                "message": "High-priority lead - call scheduled",
                "metadata": {
                    "action": "call",
                    "scheduled_for": (datetime.utcnow() + timedelta(minutes=30)).isoformat(),
                    "reason": "high_priority_lead"
                }
            })
        
        return {
            "lead": lead,
            "products": products,
            "ai_categorization": ai_result["output"],
            "assignment": assignment,
            "email_sent": email_result["success"]
        }


# Initialize service
lead_service = None

def get_lead_service() -> LeadService:
    """Get or create lead service instance"""
    global lead_service
    if lead_service is None:
        lead_service = LeadService()
    return lead_service
```

- [ ] Lead service file created
- [ ] End-to-end workflow implemented
- [ ] Test lead creation successful

---

## DAY 5-6: API Endpoints Implementation

### Step 4: Create Lead API Endpoints (90 minutes)

**Objective**: Implement all lead-related API endpoints

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\api\leads.py`

**Implementation**:

```python
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.lead import (
    LeadSubmission,
    Lead,
    LeadWithProducts,
    LeadUpdate,
    LeadStatusUpdate
)
from app.services.lead_service import get_lead_service
from app.utils.db import query_records, get_record, update_record, get_lead_full

router = APIRouter(prefix="/api/leads", tags=["leads"])

@router.post("/", response_model=Dict)
async def create_lead(submission: LeadSubmission):
    """
    Capture new lead from website form
    
    This triggers the complete automation workflow:
    1. Store lead and products
    2. AI categorization
    3. Auto-assignment
    4. Send acknowledgement email
    5. Create follow-up tasks
    """
    try:
        lead_service = get_lead_service()
        result = await lead_service.create_lead_with_products(
            lead_data=submission.dict(exclude={"product_interests"}),
            product_interests=[p.dict() for p in submission.product_interests]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Lead])
async def list_leads(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """List all leads with optional filtering"""
    filters = {}
    if status:
        filters["status"] = status
    
    leads = await query_records(
        "leads",
        filters=filters,
        order_by="created_at.desc",
        limit=limit
    )
    return leads


@router.get("/{lead_id}")
async def get_lead_details(lead_id: str):
    """Get complete lead details including products and activities"""
    full_lead = await get_lead_full(lead_id)
    if not full_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return full_lead


@router.put("/{lead_id}", response_model=Lead)
async def update_lead(lead_id: str, lead_update: LeadUpdate):
    """Update lead information"""
    updated = await update_record(
        "leads",
        lead_id,
        lead_update.dict(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated


@router.put("/{lead_id}/status")
async def update_lead_status(lead_id: str, status_update: LeadStatusUpdate):
    """Update lead status and log activity"""
    # Update status
    await update_record("leads", lead_id, {"status": status_update.status})
    
    # Log status change activity
    await insert_record("lead_activity", {
        "lead_id": lead_id,
        "type": "status_change",
        "status": "completed",
        "message": f"Status changed to {status_update.status}",
        "actor_type": "user",
        "metadata": {"new_status": status_update.status}
    })
    
    return {"success": True, "new_status": status_update.status}


@router.post("/{lead_id}/recategorize")
async def recategorize_lead(lead_id: str):
    """Manually trigger AI re-categorization"""
    lead = await get_record("leads", lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get AI service and recategorize
    ai_service = get_ai_service()
    ai_result = await ai_service.categorize_lead({
        "role": lead.get("role"),
        "location": lead.get("location"),
        "message": lead.get("message")
    })
    
    # Log new AI result
    await insert_record("lead_activity", {
        "lead_id": lead_id,
        "type": "ai_result",
        "status": "completed",
        "message": "Manual re-categorization requested",
        "actor_type": "user",
        "metadata": ai_result
    })
    
    return ai_result
```

**Register Router in Main**:

Update `app/main.py`:
```python
from app.api import leads

app.include_router(leads.router)
```

- [ ] Lead API endpoints created
- [ ] Router registered in main.py
- [ ] Test POST /api/leads
- [ ] Test GET /api/leads
- [ ] Test GET /api/leads/{id}

---

### Step 5: Create Analytics API Endpoints (45 minutes)

**Objective**: Implement analytics and dashboard endpoints

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\api\analytics.py`

**Implementation**:

```python
from fastapi import APIRouter
from app.utils.db import get_dashboard_stats, execute_rpc, query_records

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard():
    """Get dashboard statistics"""
    stats = await get_dashboard_stats()
    return stats


@router.get("/conversion")
async def get_conversion_funnel():
    """Get conversion funnel data"""
    # Query leads grouped by status
    leads = await query_records("leads")
    
    funnel = {
        "new": len([l for l in leads if l["status"] == "new"]),
        "contacted": len([l for l in leads if l["status"] == "contacted"]),
        "nurturing": len([l for l in leads if l["status"] == "nurturing"]),
        "qualified": len([l for l in leads if l["status"] == "qualified"]),
        "converted": len([l for l in leads if l["status"] == "converted"]),
        "lost": len([l for l in leads if l["status"] == "lost"])
    }
    
    return funnel


@router.get("/sla-performance")
async def get_sla_performance():
    """Get SLA performance metrics"""
    assignments = await query_records("assignments")
    
    completed = [a for a in assignments if a["completed_at"] is not None]
    
    if not completed:
        return {
            "total_assignments": len(assignments),
            "completed": 0,
            "sla_met_rate": 0,
            "avg_response_time_minutes": 0
        }
    
    sla_met_count = len([a for a in completed if a.get("sla_met")])
    
    return {
        "total_assignments": len(assignments),
        "completed": len(completed),
        "sla_met_rate": round((sla_met_count / len(completed)) * 100, 2),
        "avg_response_time_minutes": round(
            sum([a.get("response_time_minutes", 0) for a in completed]) / len(completed),
            0
        )
    }
```

**Register Router**:
```python
# In main.py
from app.api import analytics
app.include_router(analytics.router)
```

- [ ] Analytics endpoints created
- [ ] Router registered
- [ ] Test dashboard endpoint
- [ ] Test conversion funnel
- [ ] Test SLA performance

---

### Step 6: Create Follow-up and Approval Endpoints (60 minutes)

**Objective**: Implement follow-up and approval management endpoints

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\api\approvals.py`

**Implementation**:

```python
from fastapi import APIRouter, HTTPException
from typing import List
from app.utils.db import (
    query_records,
    get_record,
    update_record,
    insert_record,
    get_pending_follow_ups
)

router = APIRouter(prefix="/api", tags=["approvals"])

# Follow-ups
@router.get("/follow-ups/pending")
async def list_pending_follow_ups():
    """Get all pending follow-ups"""
    follow_ups = await get_pending_follow_ups()
    return follow_ups


@router.post("/follow-ups/{activity_id}/complete")
async def complete_follow_up(activity_id: str):
    """Mark follow-up as completed"""
    await update_record("lead_activity", activity_id, {
        "status": "completed"
    })
    return {"success": True}


@router.put("/follow-ups/{activity_id}/snooze")
async def snooze_follow_up(activity_id: str, minutes: int = 60):
    """Snooze follow-up by specified minutes"""
    from datetime import datetime, timedelta
    
    activity = await get_record("lead_activity", activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    metadata = activity.get("metadata", {})
    current_time = datetime.fromisoformat(metadata.get("scheduled_for", datetime.utcnow().isoformat()))
    new_time = current_time + timedelta(minutes=minutes)
    
    metadata["scheduled_for"] = new_time.isoformat()
    metadata["snoozed"] = True
    
    await update_record("lead_activity", activity_id, {"metadata": metadata})
    return {"success": True, "new_time": new_time.isoformat()}


# Approvals
@router.get("/approvals/pending")
async def list_pending_approvals():
    """Get all pending approvals"""
    approvals = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "pending"},
        order_by="created_at.desc"
    )
    return approvals


@router.post("/approvals/{activity_id}/approve")
async def approve_request(activity_id: str, notes: str = ""):
    """Approve an approval request"""
    await update_record("lead_activity", activity_id, {
        "status": "approved"
    })
    
    # Log approval action
    activity = await get_record("lead_activity", activity_id)
    await insert_record("lead_activity", {
        "lead_id": activity["lead_id"],
        "type": "note",
        "status": "completed",
        "message": f"Approval granted: {notes}",
        "actor_type": "user"
    })
    
    return {"success": True, "status": "approved"}


@router.post("/approvals/{activity_id}/reject")
async def reject_request(activity_id: str, reason: str):
    """Reject an approval request"""
    await update_record("lead_activity", activity_id, {
        "status": "rejected"
    })
    
    # Log rejection
    activity = await get_record("lead_activity", activity_id)
    await insert_record("lead_activity", {
        "lead_id": activity["lead_id"],
        "type": "note",
        "status": "completed",
        "message": f"Approval rejected: {reason}",
        "actor_type": "user"
    })
    
    return {"success": True, "status": "rejected"}
```

**Register Router**:
```python
# In main.py
from app.api import approvals
app.include_router(approvals.router)
```

- [ ] Follow-up endpoints created
- [ ] Approval endpoints created
- [ ] Router registered
- [ ] Test pending follow-ups
- [ ] Test approve/reject

---

## DAY 7: Testing & Integration

### Step 7: End-to-End Testing (120 minutes)

**Objective**: Test complete lead capture workflow

**Test Script**: `b:\Project\SaaS\Second\lead-automation-backend\test_workflow.py`

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    """Test complete lead capture workflow"""
    
    print("=== Testing Complete Lead Workflow ===\n")
    
    # Step 1: Create lead
    print("1. Creating new lead...")
    lead_data = {
        "name": "Rajesh Kumar",
        "email": "rajesh@example.com",
        "phone": "+91 9876543210",
        "role": "Builder",
        "location": "Delhi",
        "message": "Need urgent quote for 5000 sq ft commercial project",
        "product_interests": [
            {"category": "Flooring", "product": "Commercial Grade Flooring"},
            {"category": "Lighting", "product": "LED Panel Lights"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/leads", json=lead_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Lead ID: {result['lead']['id']}")
    print(f"AI Priority: {result['ai_categorization']['priority']}")
    print(f"Email Sent: {result['email_sent']}\n")
    
    lead_id = result['lead']['id']
    
    # Step 2: Get lead details
    print("2. Fetching lead details...")
    response = requests.get(f"{BASE_URL}/api/leads/{lead_id}")
    full_lead = response.json()
    print(f"Products: {len(full_lead['products'])}")
    print(f"Activities: {len(full_lead['activities'])}")
    print(f"Pending Follow-ups: {len(full_lead['pending_follow_ups'] or [])}\n")
    
    # Step 3: Check dashboard
    print("3. Checking dashboard stats...")
    response = requests.get(f"{BASE_URL}/api/analytics/dashboard")
    stats = response.json()
    print(f"Total Leads: {stats['total_leads']}")
    print(f"New Today: {stats['new_leads_today']}")
    print(f"Pending Follow-ups: {stats['pending_follow_ups']}\n")
    
    # Step 4: Check pending follow-ups
    print("4. Checking pending follow-ups...")
    response = requests.get(f"{BASE_URL}/api/follow-ups/pending")
    follow_ups = response.json()
    print(f"Found {len(follow_ups)} pending follow-ups\n")
    
    print("=== Workflow Test Complete ===")

if __name__ == "__main__":
    test_complete_workflow()
```

**Run Test**:
```bash
.\venv\Scripts\Activate.ps1
python test_workflow.py
```

**Expected Output**:
```
=== Testing Complete Lead Workflow ===

1. Creating new lead...
Status: 200
Lead ID: <uuid>
AI Priority: high
Email Sent: True

2. Fetching lead details...
Products: 2
Activities: 4
Pending Follow-ups: 1

3. Checking dashboard stats...
Total Leads: 2
New Today: 1
Pending Follow-ups: 2

4. Checking pending follow-ups...
Found 2 pending follow-ups

=== Workflow Test Complete ===
```

- [ ] Test script created
- [ ] Workflow test passes
- [ ] All steps execute successfully

---

### Step 8: Update Documentation and Health Checks (30 minutes)

**Objective**: Add API documentation and update health checks

**Update Health Check** in `app/main.py`:

```python
@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    from app.utils.db import get_dashboard_stats
    from app.services.ai_service import get_ai_service
    from app.services.email_service import get_email_service
    
    # Test database
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
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "services": {
            "api": "operational",
            "database": db_status,
            "supabase": "operational" if db_connected else "error",
            "groq": ai_status,
            "resend": email_status
        },
        "database_stats": db_stats if db_connected else None
    }
```

**Add API Documentation**:

Update `app/main.py`:
```python
app = FastAPI(
    title="Lead Automation API",
    version="1.0.0",
    description="""
    AI-Powered Lead Management Automation System
    
    ## Features
    * Automated lead capture with AI categorization
    * Email automation via Resend
    * SLA tracking and enforcement
    * Follow-up scheduling
    * Approval workflows
    * Real-time analytics
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)
```

- [ ] Health check updated with all services
- [ ] API documentation added
- [ ] Swagger docs accessible at /docs

---

## 🎯 Phase 4 Completion Checklist

### Service Layer ✅
- [ ] AI Service implemented (Groq integration)
- [ ] Email Service implemented (Resend integration)
- [ ] Lead Service with business logic
- [ ] All services tested individually

### API Endpoints ✅
- [ ] Lead endpoints (POST, GET, PUT)
- [ ] Analytics endpoints (dashboard, conversion, SLA)
- [ ] Follow-up endpoints (list, complete, snooze)
- [ ] Approval endpoints (list, approve, reject)
- [ ] All endpoints registered and tested

### Business Logic ✅
- [ ] Lead capture workflow working end-to-end
- [ ] AI categorization with fallback
- [ ] Auto-assignment implemented
- [ ] Email acknowledgement working
- [ ] Follow-up creation for high-priority leads

### Testing ✅
- [ ] End-to-end workflow test passes
- [ ] All API endpoints return correct data
- [ ] Health check shows all services operational
- [ ] Error handling tested

---

## 📁 Files Created/Modified

### New Service Files
1. **`app/services/ai_service.py`** - Groq AI integration
2. **`app/services/email_service.py`** - Resend email integration
3. **`app/services/lead_service.py`** - Business logic layer

### New API Files
4. **`app/api/leads.py`** - Lead endpoints
5. **`app/api/analytics.py`** - Analytics endpoints
6. **`app/api/approvals.py`** - Follow-up & approval endpoints

### Test Files
7. **`test_workflow.py`** - End-to-end workflow tests

### Modified Files
8. **`app/main.py`** - Router registration, health check, docs
9. **`requirements.txt`** - Added groq and resend packages

---

## 🚀 Dependencies to Install

```bash
# In backend virtual environment
.\venv\Scripts\Activate.ps1

pip install groq
pip install resend
```

---

## 🔍 Verification Steps

### 1. Test AI Service
```bash
python -c "from app.services.ai_service import get_ai_service; import asyncio; asyncio.run(get_ai_service().categorize_lead({'role': 'Architect', 'message': 'Need quote'}))"
```

### 2. Test Email Service
```bash
python -c "from app.services.email_service import get_email_service; import asyncio; asyncio.run(get_email_service().send_acknowledgement('test@example.com', 'Test', ['Flooring']))"
```

### 3. Test Complete Workflow
```bash
python test_workflow.py
```

### 4. Check Health Endpoint
Visit: http://localhost:8000/health

Should show:
```json
{
  "status": "healthy",
  "services": {
    "api": "operational",
    "database": "operational",
    "supabase": "operational",
    "groq": "operational",
    "resend": "operational"
  }
}
```

### 5. Test API via Swagger
Visit: http://localhost:8000/docs

Test endpoints interactively

---

## 📝 Notes

- AI service has retry logic (3 attempts) and fallback to rule-based categorization
- Email service logs all attempts in lead_activity table
- Lead service implements complete automation workflow
- All services use singleton pattern for efficiency
- Error handling at every layer
- Logging configured for debugging

**Phase 4 Status: Ready for Implementation** 

---

## 🎯 What's Next: Phase 5

Once Phase 4 is complete, we'll move to:

**Phase 5: Frontend Development**
- Build React components
- Implement lead form
- Create admin dashboard
- Add real-time updates
- Connect to backend APIs
