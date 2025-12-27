from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# ============================================
# ASSIGNMENT MODELS
# ============================================

class AssignmentBase(BaseModel):
    """Base assignment model"""
    owner_id: str = Field(..., max_length=255)
    owner_name: Optional[str] = Field(None, max_length=255)
    sla_deadline: datetime


class AssignmentCreate(AssignmentBase):
    """Model for creating assignment"""
    lead_id: UUID


class AssignmentUpdate(BaseModel):
    """Model for updating assignment"""
    status: Optional[str] = None  # active, completed, reassigned
    completed_at: Optional[datetime] = None


class Assignment(AssignmentBase):
    """Complete assignment model (from database)"""
    id: UUID
    lead_id: UUID
    assigned_at: datetime
    sla_met: Optional[bool] = None
    response_time_minutes: Optional[int] = None
    status: str
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssignmentComplete(BaseModel):
    """Model for completing an assignment"""
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "completed_at": "2024-12-27T12:00:00Z"
            }
        }


class AssignmentReassign(BaseModel):
    """Model for reassigning a lead"""
    new_owner_id: str = Field(..., max_length=255)
    new_owner_name: str = Field(..., max_length=255)
    new_sla_deadline: datetime
    reason: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_owner_id": "sales_user_10",
                "new_owner_name": "Rajesh Kumar",
                "new_sla_deadline": "2024-12-27T18:00:00Z",
                "reason": "Specialization in commercial projects"
            }
        }


class SLAViolation(BaseModel):
    """Model for SLA violation information"""
    assignment_id: UUID
    lead_id: UUID
    owner_id: str
    owner_name: str
    sla_deadline: datetime
    minutes_overdue: int
    
    class Config:
        from_attributes = True
