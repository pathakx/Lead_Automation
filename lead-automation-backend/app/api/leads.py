from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from app.models.lead import (
    LeadSubmission,
    Lead,
    LeadUpdate,
    LeadStatusUpdate
)
from app.services.lead_service import get_lead_service
from app.services.ai_service import get_ai_service
from app.utils.db import (
    query_records,
    get_record,
    update_record,
    get_lead_full,
    insert_record
)

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("/", response_model=Dict[str, Any])
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
    
    # Get products for this lead
    products = await query_records("lead_products", filters={"lead_id": lead_id})
    
    # Get AI service and recategorize
    ai_service = get_ai_service()
    ai_result = await ai_service.categorize_lead({
        "role": lead.get("role"),
        "location": lead.get("location"),
        "products": [p["product"] for p in products],
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
