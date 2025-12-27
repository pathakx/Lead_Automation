from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.utils.db import query_records, update_record, get_record
from datetime import datetime

router = APIRouter(prefix="/api/follow-ups", tags=["follow-ups"])


@router.get("/pending")
async def get_pending_follow_ups():
    """
    Get all pending follow-up tasks with lead details
    Returns follow-ups that need action
    """
    try:
        print("=" * 60)
        print("DEBUG: Follow-ups endpoint called")
        
        # Query pending follow-ups from lead_activity table
        follow_ups = await query_records(
            "lead_activity",
            filters={"type": "follow_up", "status": "pending"},
            order_by="created_at",
            limit=100
        )
        
        print(f"DEBUG: Found {len(follow_ups)} follow-ups in database")
        
        # Enrich with lead details
        enriched_follow_ups = []
        for idx, follow_up in enumerate(follow_ups):
            lead_id = follow_up.get("lead_id")
            print(f"DEBUG: Processing follow-up {idx+1}/{len(follow_ups)} for lead {lead_id}")
            
            # Get lead details
            lead = await get_record("leads", lead_id)
            if not lead:
                print(f"DEBUG: Lead {lead_id} not found, skipping")
                continue
            
            print(f"DEBUG: Found lead: {lead.get('name')} - {lead.get('email')}")
            
            # Get products for this lead
            products = await query_records(
                "lead_products",
                filters={"lead_id": lead_id}
            )
            
            enriched_data = {
                "id": follow_up["id"],
                "lead_id": lead_id,
                "lead_name": lead.get("name"),
                "lead_email": lead.get("email"),
                "lead_phone": lead.get("phone"),
                "lead_company": lead.get("company"),
                "lead_role": lead.get("role"),
                "lead_status": lead.get("status"),
                "message": follow_up.get("message"),
                "scheduled_for": follow_up.get("metadata", {}).get("scheduled_for"),
                "action": follow_up.get("metadata", {}).get("action"),
                "reason": follow_up.get("metadata", {}).get("reason"),
                "products": [p.get("product") for p in products],
                "created_at": follow_up.get("created_at"),
                "metadata": follow_up.get("metadata")
            }
            
            print(f"DEBUG: Enriched data created for {lead.get('name')}")
            enriched_follow_ups.append(enriched_data)
        
        print(f"DEBUG: Returning {len(enriched_follow_ups)} enriched follow-ups")
        print("=" * 60)
        
        return enriched_follow_ups
        
    except Exception as e:
        print(f"ERROR in follow-ups endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


async def enrich_follow_ups(follow_ups: List[Dict]) -> List[Dict]:
    """Helper function to enrich follow-ups with lead details"""
    enriched = []
    for follow_up in follow_ups:
        lead_id = follow_up.get("lead_id")
        lead = await get_record("leads", lead_id)
        if not lead:
            continue
        
        products = await query_records("lead_products", filters={"lead_id": lead_id})
        
        enriched.append({
            "id": follow_up["id"],
            "lead_id": lead_id,
            "lead_name": lead.get("name"),
            "lead_email": lead.get("email"),
            "lead_phone": lead.get("phone"),
            "lead_company": lead.get("company"),
            "lead_role": lead.get("role"),
            "lead_status": lead.get("status"),
            "message": follow_up.get("message"),
            "scheduled_for": follow_up.get("metadata", {}).get("scheduled_for"),
            "action": follow_up.get("metadata", {}).get("action"),
            "reason": follow_up.get("metadata", {}).get("reason"),
            "products": [p.get("product") for p in products],
            "created_at": follow_up.get("created_at"),
            "metadata": follow_up.get("metadata"),
            "status": follow_up.get("status")
        })
    
    return enriched


@router.get("/completed")
async def get_completed_follow_ups():
    """
    Get all completed follow-up tasks
    Returns follow-ups that have been marked as complete
    """
    try:
        follow_ups = await query_records(
            "lead_activity",
            filters={"type": "follow_up", "status": "completed"},
            order_by="created_at.desc",
            limit=100
        )
        return await enrich_follow_ups(follow_ups)
    except Exception as e:
        print(f"ERROR in completed follow-ups endpoint: {str(e)}")
        return []


@router.get("/snoozed")
async def get_snoozed_follow_ups():
    """
    Get all snoozed follow-up tasks
    Returns follow-ups that have been snoozed
    """
    try:
        # Get all pending follow-ups
        all_pending = await query_records(
            "lead_activity",
            filters={"type": "follow_up", "status": "pending"},
            order_by="created_at.desc",
            limit=100
        )
        
        # Filter only snoozed ones (check metadata)
        snoozed = [fu for fu in all_pending if fu.get("metadata", {}).get("snoozed") == True]
        
        return await enrich_follow_ups(snoozed)
    except Exception as e:
        print(f"ERROR in snoozed follow-ups endpoint: {str(e)}")
        return []


@router.get("/stats")
async def get_follow_up_stats():
    """
    Get follow-up statistics
    Returns counts of pending, completed, and snoozed follow-ups
    """
    try:
        # Get all follow-ups
        all_followups = await query_records(
            "lead_activity",
            filters={"type": "follow_up"}
        )
        
        pending = [fu for fu in all_followups if fu.get("status") == "pending" and not fu.get("metadata", {}).get("snoozed")]
        completed = [fu for fu in all_followups if fu.get("status") == "completed"]
        snoozed = [fu for fu in all_followups if fu.get("status") == "pending" and fu.get("metadata", {}).get("snoozed")]
        
        # Count by priority for pending
        high = len([fu for fu in pending if fu.get("metadata", {}).get("priority") == "high"])
        medium = len([fu for fu in pending if fu.get("metadata", {}).get("priority") == "medium"])
        low = len([fu for fu in pending if fu.get("metadata", {}).get("priority") == "low"])
        
        return {
            "pending": len(pending),
            "completed": len(completed),
            "snoozed": len(snoozed),
            "high": high,
            "medium": medium,
            "low": low,
            "total": len(all_followups)
        }
    except Exception as e:
        print(f"ERROR in stats endpoint: {str(e)}")
        return {
            "pending": 0,
            "completed": 0,
            "snoozed": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "total": 0
        }


@router.post("/{follow_up_id}/complete")
async def complete_follow_up(follow_up_id: str, request_data: Dict[str, Any] = {}):
    """Mark a follow-up as completed"""
    
    notes = request_data.get("notes", "") if request_data else ""
    
    follow_up = await get_record("lead_activity", follow_up_id)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    # Update status to completed
    await update_record("lead_activity", follow_up_id, {
        "status": "completed",
        "metadata": {
            **follow_up.get("metadata", {}),
            "completed_at": datetime.utcnow().isoformat(),
            "completion_notes": notes
        }
    })
    
    return {"success": True, "message": "Follow-up marked as completed"}


@router.post("/{follow_up_id}/snooze")
async def snooze_follow_up(follow_up_id: str, request_data: Dict[str, Any]):
    """Snooze a follow-up to a later time"""
    
    snooze_until = request_data.get("snooze_until")
    if not snooze_until:
        raise HTTPException(status_code=400, detail="snooze_until is required")
    
    follow_up = await get_record("lead_activity", follow_up_id)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    # Update scheduled time and mark as snoozed
    await update_record("lead_activity", follow_up_id, {
        "metadata": {
            **follow_up.get("metadata", {}),
            "scheduled_for": snooze_until,
            "snoozed": True,
            "snoozed_at": datetime.utcnow().isoformat()
        }
    })
    
    return {"success": True, "message": f"Follow-up snoozed until {snooze_until}"}

