from fastapi import APIRouter
from typing import Dict, Any
from app.utils.db import get_dashboard_stats, query_records

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard() -> Dict[str, Any]:
    """
    Get dashboard statistics
    
    Returns:
    - total_leads
    - new_leads_today
    - pending_follow_ups
    - pending_approvals
    - sla_violations
    - avg_response_time_minutes
    - conversion_rate
    """
    stats = await get_dashboard_stats()
    return stats


@router.get("/conversion")
async def get_conversion_funnel() -> Dict[str, int]:
    """
    Get conversion funnel data
    
    Returns count of leads at each status stage
    """
    # Query all leads
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
async def get_sla_performance() -> Dict[str, Any]:
    """
    Get SLA performance metrics
    
    Returns:
    - total_assignments
    - completed
    - sla_met_rate (percentage)
    - avg_response_time_minutes
    """
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
