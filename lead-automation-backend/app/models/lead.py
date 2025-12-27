from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ============================================
# LEAD MODELS
# ============================================

class LeadBase(BaseModel):
    """Base lead model with source data fields"""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=255)
    role: Optional[str] = Field(None, max_length=100)  # Home Owner, Architect, etc.
    location: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None
    source: str = Field(default="website_form", max_length=100)


class LeadCreate(LeadBase):
    """Model for creating a new lead"""
    pass


class LeadUpdate(BaseModel):
    """Model for updating lead fields"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None  # new, contacted, nurturing, qualified, converted, lost


class LeadStatusUpdate(BaseModel):
    """Model for status-only updates"""
    status: str = Field(..., pattern="^(new|contacted|nurturing|qualified|converted|lost)$")


class Lead(LeadBase):
    """Complete lead model (from database)"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    status: str
    first_response_at: Optional[datetime] = None
    last_contact_at: Optional[datetime] = None
    conversion_date: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


# ============================================
# LEAD PRODUCT MODELS
# ============================================

class LeadProductBase(BaseModel):
    """Base product model"""
    category: str = Field(..., max_length=100)  # Flooring, Wall, Lighting, Laminates
    product: str = Field(..., max_length=255)
    quantity: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class LeadProductCreate(LeadProductBase):
    """Model for creating product interest"""
    pass


class LeadProduct(LeadProductBase):
    """Complete product model (from database)"""
    id: UUID
    lead_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# COMPOSITE MODELS
# ============================================

class LeadWithProducts(Lead):
    """Lead with associated products"""
    products: List[LeadProduct] = []


class LeadSubmission(BaseModel):
    """Model for website form submission (lead + products)"""
    # Lead info
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    message: Optional[str] = None
    source: str = "website_form"
    
    # Product interests
    product_interests: List[LeadProductBase] = Field(default_factory=list)
