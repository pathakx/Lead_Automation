from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.utils.db import (
    query_records,
    get_record,
    update_record,
    insert_record,
    get_pending_follow_ups
)

router = APIRouter(prefix="/api", tags=["approvals"])



# ============================================
# APPROVAL ENDPOINTS
# ============================================

@router.get("/approvals/pending")
async def list_pending_approvals() -> List[Dict[str, Any]]:
    """
    Get all pending approvals
    
    Returns activities with type='approval' and status='pending'
    """
    approvals = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "pending"},
        order_by="created_at.desc"
    )
    return approvals


@router.get("/approvals/approved")
async def list_approved_approvals() -> List[Dict[str, Any]]:
    """
    Get all approved approvals (history)
    
    Returns activities with type='approval' and status='approved'
    """
    approvals = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "approved"},
        order_by="created_at.desc",
        limit=100
    )
    return approvals


@router.get("/approvals/rejected")
async def list_rejected_approvals() -> List[Dict[str, Any]]:
    """
    Get all rejected approvals (history)
    
    Returns activities with type='approval' and status='rejected'
    """
    approvals = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "rejected"},
        order_by="created_at.desc",
        limit=100
    )
    return approvals


@router.get("/approvals/stats")
async def get_approval_stats() -> Dict[str, int]:
    """
    Get approval statistics
    
    Returns counts of pending, approved, and rejected approvals
    """
    pending = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "pending"}
    )
    
    approved = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "approved"}
    )
    
    rejected = await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "rejected"}
    )
    
    return {
        "pending": len(pending),
        "approved": len(approved),
        "rejected": len(rejected),
        "total": len(pending) + len(approved) + len(rejected)
    }


@router.post("/approvals/{activity_id}/approve")
async def approve_request(
    activity_id: str,
    request_data: Dict[str, Any] = {}
) -> Dict[str, Any]:
    """
    Approve an approval request
    
    Args:
    - activity_id: ID of the approval activity
    - request_data: { "notes": "optional approval notes" }
    """
    notes = request_data.get("notes", "") if request_data else ""
    
    activity = await get_record("lead_activity", activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    # Update approval status to approved
    await update_record("lead_activity", activity_id, {
        "status": "approved"
    })
    
    # Log approval action
    await insert_record("lead_activity", {
        "lead_id": activity["lead_id"],
        "type": "note",
        "status": "completed",
        "message": f"Approval granted: {notes}" if notes else "Approval granted",
        "actor_type": "user",
        "metadata": {
            "approval_notes": notes,
            "approved_at": datetime.utcnow().isoformat(),
            "approval_type": activity.get("metadata", {}).get("approval_type")
        }
    })
    
    return {
        "success": True,
        "status": "approved",
        "notes": notes
    }


@router.post("/approvals/{activity_id}/reject")
async def reject_request(
    activity_id: str,
    request_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Reject an approval request
    
    Args:
    - activity_id: ID of the approval activity
    - request_data: { "reason": "rejection reason" }
    """
    reason = request_data.get("reason", "")
    
    if not reason:
        raise HTTPException(status_code=400, detail="Rejection reason is required")
    
    activity = await get_record("lead_activity", activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    # Update approval status to rejected
    await update_record("lead_activity", activity_id, {
        "status": "rejected"
    })
    
    # Log rejection as a note
    await insert_record("lead_activity", {
        "lead_id": activity["lead_id"],
        "type": "note",
        "status": "completed",
        "message": f"Approval rejected: {reason}",
        "actor_type": "user",
        "metadata": {
            "rejection_reason": reason,
            "rejected_at": datetime.utcnow().isoformat(),
            "approval_type": activity.get("metadata", {}).get("approval_type")
        }
    })
    
    return {
        "success": True,
        "status": "rejected",
        "reason": reason
    }
