from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# ============================================
# LEAD ACTIVITY MODELS
# ============================================

class LeadActivityBase(BaseModel):
    """Base activity model"""
    type: str = Field(..., max_length=50)  # ai_result, assignment, email, etc.
    status: str = Field(default="completed", max_length=50)
    message: str
    actor_type: str = Field(default="system", max_length=50)
    actor_id: Optional[str] = Field(None, max_length=255)
    metadata: Optional[Dict[str, Any]] = None


class LeadActivityCreate(LeadActivityBase):
    """Model for creating activity"""
    lead_id: UUID


class LeadActivity(LeadActivityBase):
    """Complete activity model (from database)"""
    id: UUID
    lead_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadActivityUpdate(BaseModel):
    """Model for updating activity (mainly status)"""
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ============================================
# SPECIFIC ACTIVITY TYPES (for metadata validation)
# ============================================

class AIResultActivity(BaseModel):
    """AI analysis result metadata"""
    intent: str  # quote_request, general_inquiry, etc.
    lead_type: str  # home_owner, architect, builder, contractor
    priority: str  # low, medium, high
    suggested_action: str  # call_within_30_min, email_quote, etc.
    reasoning: Optional[str] = None
    model: str  # llama-3.1-70b-versatile
    prompt_version: str  # v1.0, v1.1, etc.
    
    class Config:
        json_schema_extra = {
            "example": {
                "intent": "quote_request",
                "lead_type": "architect",
                "priority": "high",
                "suggested_action": "call_within_30_min",
                "reasoning": "High-value commercial project",
                "model": "llama-3.1-70b-versatile",
                "prompt_version": "v1.0"
            }
        }


class FollowUpActivity(BaseModel):
    """Follow-up activity metadata"""
    action: str  # call, email, meeting
    scheduled_for: datetime
    reason: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "action": "call",
                "scheduled_for": "2024-12-27T15:30:00Z",
                "reason": "high_priority_lead"
            }
        }


class ApprovalActivity(BaseModel):
    """Approval request metadata"""
    approval_type: str  # high_value_lead, special_discount, etc.
    ai_recommendation: Optional[str] = None
    requires_manager: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "approval_type": "high_value_lead",
                "ai_recommendation": "Approve immediate callback",
                "requires_manager": True
            }
        }


class EmailActivity(BaseModel):
    """Email activity metadata"""
    template: str  # acknowledgement, quote, follow_up
    channel: str = "resend"
    resend_id: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "template": "acknowledgement",
                "channel": "resend",
                "resend_id": "msg_abc123"
            }
        }


class AssignmentActivityMetadata(BaseModel):
    """Assignment activity metadata"""
    assigned_by: str  # system, user_id
    owner_id: str
    owner_name: str
    sla_deadline: str  # ISO timestamp as string
    
    class Config:
        json_schema_extra = {
            "example": {
                "assigned_by": "system",
                "owner_id": "sales_user_5",
                "owner_name": "Neha Patel",
                "sla_deadline": "2024-12-27T16:00:00Z"
            }
        }


class StatusChangeActivity(BaseModel):
    """Status change activity metadata"""
    old_status: str
    new_status: str
    changed_by: str  # user_id or system
    reason: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_status": "new",
                "new_status": "contacted",
                "changed_by": "sales_user_5",
                "reason": "Initial contact made"
            }
        }
