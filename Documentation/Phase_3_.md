# Phase 3: Database Schema & Models - Master Plan
## AI-Powered Lead Management Automation System

---

## 📅 Timeline: Days 3-4
**Status**: 🚀 Ready for Implementation  
**Last Updated**: December 27, 2024  
**Prerequisites**: Phase 2 completed (Frontend & Backend infrastructure ready)

---

## 🎯 Phase 3 Objectives

### Primary Goal
Design and implement the complete database schema on Supabase, create Pydantic models for data validation, and establish database utilities for seamless backend-database communication using the event-sourcing pattern.

### Success Criteria
- ✅ All 4 core tables created in Supabase
- ✅ Row Level Security (RLS) policies configured
- ✅ Database indexes optimized for performance
- ✅ Database functions and triggers created
- ✅ Pydantic models created for all tables
- ✅ Database utility functions implemented
- ✅ Sample data inserted for testing
- ✅ Database queries verified
- ✅ Event-sourcing pattern implemented

---

## 📋 Deliverables

### 1. Database Schema
- ✅ `leads` table (source data only - NO AI fields)
- ✅ `lead_products` table (product interests)
- ✅ `lead_activity` table (event log - AI results, follow-ups, approvals)
- ✅ `assignments` table (owner & SLA tracking)

### 2. Database Security & Performance
- ✅ Row Level Security (RLS) policies
- ✅ Database indexes for performance
- ✅ Foreign key constraints
- ✅ Triggers for SLA calculation

### 3. Database Functions
- ✅ `get_lead_full()` - Get complete lead with all relationships
- ✅ `get_dashboard_stats()` - Get dashboard statistics
- ✅ `get_pending_follow_ups()` - Get pending follow-ups
- ✅ SLA checking trigger

### 4. Backend Models
- ✅ Pydantic models for all tables
- ✅ Request/Response schemas
- ✅ Validation logic

### 5. Database Utilities
- ✅ Supabase client configuration
- ✅ Database helper functions
- ✅ Error handling

---

## 🏗️ Database Design Philosophy

### Event-Sourcing Pattern ⭐

**Core Principle**: Keep source data pure. Store ALL AI results, follow-ups, and approvals as activities in the `lead_activity` table.

**✅ DO:**
- Store raw form data in `leads` table
- Store all AI analysis in `lead_activity` with type='ai_result'
- Store follow-ups as activities with type='follow_up', status='pending'
- Store approvals as activities with type='approval', status='pending'
- Use `metadata` JSONB field for flexible activity-specific data
- Always store model version and prompt version in AI results

**❌ DON'T:**
- Pollute `leads` table with AI-generated fields
- Create separate tables for tasks/approvals (use activities instead)
- Update `leads` table with AI categorization
- Store computed values that can be derived from events

---

## 📝 Detailed Implementation Steps

## DAY 3: Database Schema Creation

### Step 1: Verify Supabase Project Access (10 minutes)

**Objective**: Ensure you can access your Supabase project and run SQL commands

**Tasks**:
1. Open Supabase dashboard: https://app.supabase.com
2. Select your project: `lead-automation-db`
3. Navigate to **SQL Editor** (left sidebar)
4. Test connection by running:
   ```sql
   SELECT version();
   ```
5. Verify you have admin access

**Verification**:
- [ ] Can access Supabase project
- [ ] SQL Editor is accessible
- [ ] Test query returns PostgreSQL version

---

### Step 2: Enable UUID Extension (5 minutes)

**Objective**: Enable UUID generation for primary keys

**SQL Command**:

Go to SQL Editor and run:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify extension is enabled
SELECT * FROM pg_extension WHERE extname = 'uuid-ossp';
```

**Expected Result**: Should show `uuid-ossp` extension is installed

**Verification**:
- [ ] UUID extension enabled
- [ ] No errors in SQL execution

---

### Step 3: Create Leads Table (20 minutes)

**Objective**: Create the primary leads table with ONLY source data

**Important**: This table should contain NO AI-generated fields!

**SQL Command**:

```sql
-- ================================================
-- 1. LEADS TABLE (SOURCE DATA ONLY - NO AI POLLUTION)
-- ================================================
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Contact Information (SOURCE DATA ONLY)
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(255),
    role VARCHAR(100), -- Home Owner, Architect, Builder, Contractor
    location VARCHAR(255),
    
    -- Lead Details (SOURCE DATA ONLY)
    message TEXT,
    source VARCHAR(100) DEFAULT 'website_form', -- website_form, referral, campaign
    
    -- Status Tracking (HUMAN-SET ONLY)
    status VARCHAR(50) DEFAULT 'new', -- new, contacted, nurturing, qualified, converted, lost
    
    -- Metadata
    first_response_at TIMESTAMP,
    last_contact_at TIMESTAMP,
    conversion_date TIMESTAMP,
    
    -- Constraints
    CONSTRAINT leads_email_created_key UNIQUE (email, created_at::date)
);

-- Indexes for leads table
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX idx_leads_email ON leads(email);

-- Add helpful comments
COMMENT ON TABLE leads IS 'Stores ONLY source data from form submissions. No AI-generated fields.';
COMMENT ON COLUMN leads.status IS 'Human-set status, not AI-generated';
```

**Field Explanations**:
- `id`: UUID primary key (auto-generated)
- `created_at`: Timestamp when lead was captured
- `name`: Full name of the lead
- `email`: Email address (required)
- `phone`: Phone number (optional)
- `company`: Company name (optional)
- `role`: Type of customer (Home Owner, Architect, Builder, Contractor)
- `location`: City/region
- `message`: Original inquiry message
- `source`: Where the lead came from
- `status`: Current human-assigned status
- `first_response_at`: When we first responded
- `last_contact_at`: Last interaction time
- `conversion_date`: When lead converted to customer

**Verification**:
```sql
-- Check table was created
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'leads';

-- Check indexes
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'leads';
```

- [ ] Table created successfully
- [ ] All columns present
- [ ] Indexes created
- [ ] NO AI fields present

---

### Step 4: Create Lead Products Table (15 minutes)

**Objective**: Store product interests for each lead

**SQL Command**:

```sql
-- ================================================
-- 2. LEAD PRODUCTS TABLE (Product Interests)
-- ================================================
CREATE TABLE lead_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Product Information
    category VARCHAR(100) NOT NULL, -- Flooring, Wall, Lighting, Laminates
    product VARCHAR(255) NOT NULL,  -- Laminate Flooring, Wall Panels, etc.
    
    -- Optional Details
    quantity VARCHAR(100), -- area/units needed
    notes TEXT,
    
    -- Foreign Key
    CONSTRAINT fk_lead_products_lead FOREIGN KEY (lead_id) 
        REFERENCES leads(id) ON DELETE CASCADE
);

-- Indexes for lead_products table
CREATE INDEX idx_lead_products_lead_id ON lead_products(lead_id);
CREATE INDEX idx_lead_products_category ON lead_products(category);

COMMENT ON TABLE lead_products IS 'Stores product interests associated with each lead';
```

**Field Explanations**:
- `lead_id`: Reference to parent lead
- `category`: Product category (Flooring, Wall, Lighting, Laminates)
- `product`: Specific product name
- `quantity`: Optional quantity/area needed
- `notes`: Additional notes about this product interest
- `ON DELETE CASCADE`: When lead is deleted, products are deleted too

**Verification**:
```sql
-- Check table and foreign key
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_name='lead_products' AND  tc.constraint_type = 'FOREIGN KEY';
```

- [ ] Table created successfully
- [ ] Foreign key to leads table exists
- [ ] Cascade delete configured

---

### Step 5: Create Lead Activity Table - THE HEART OF THE SYSTEM (25 minutes)

**Objective**: Create event log table that stores EVERYTHING (AI results, follow-ups, approvals, etc.)

**This is the most important table!**

**SQL Command**:

```sql
-- ================================================
-- 3. LEAD ACTIVITY TABLE (EVENT LOG - THE HEART OF THE SYSTEM)
-- ================================================
CREATE TABLE lead_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Activity Details
    type VARCHAR(50) NOT NULL, 
    -- Types: ai_result, assignment, email, call, follow_up, approval, status_change, note
    
    status VARCHAR(50) DEFAULT 'completed',
    -- For follow_ups: pending, completed, cancelled
    -- For approvals: pending, approved, rejected
    -- For others: completed
    
    message TEXT NOT NULL,
    
    -- Actor
    actor_type VARCHAR(50) DEFAULT 'system', -- system, user, ai
    actor_id VARCHAR(255), -- User ID if manual action
    
    -- Additional Data (FLEXIBLE JSON)
    metadata JSONB,
    
    -- Foreign Key
    CONSTRAINT fk_lead_activity_lead FOREIGN KEY (lead_id) 
        REFERENCES leads(id) ON DELETE CASCADE
);

-- Indexes for lead_activity table
CREATE INDEX idx_lead_activity_lead_id ON lead_activity(lead_id);
CREATE INDEX idx_lead_activity_type ON lead_activity(type);
CREATE INDEX idx_lead_activity_status ON lead_activity(status);
CREATE INDEX idx_lead_activity_created_at ON lead_activity(created_at DESC);
CREATE INDEX idx_lead_activity_metadata ON lead_activity USING GIN (metadata);

COMMENT ON TABLE lead_activity IS 'Event log storing ALL activities: AI results, assignments, emails, follow-ups, approvals';
COMMENT ON COLUMN lead_activity.type IS 'ai_result, assignment, email, call, follow_up, approval, status_change, note';
COMMENT ON COLUMN lead_activity.metadata IS 'Flexible JSON field for activity-specific data';
```

**Activity Type Examples**:

| Type | Status | Metadata Example |
|------|--------|------------------|
| `ai_result` | `completed` | `{"intent": "quote_request", "priority": "high", "model": "llama-3.1-70b", "prompt_version": "v1.0"}` |
| `assignment` | `completed` | `{"owner_id": "user_12", "owner_name": "Rajesh", "sla_deadline": "..."}` |
| `email` | `completed` | `{"template": "acknowledgement", "channel": "resend"}` |
| `follow_up` | `pending` | `{"action": "call", "scheduled_for": "2024-12-24T11:00:00Z"}` |
| `approval` | `pending` | `{"approval_type": "high_value_lead", "requires_manager": true}` |

**Verification**:
```sql
-- Check table structure
\d lead_activity

-- Check GIN index for metadata
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'lead_activity' AND indexdef LIKE '%GIN%';
```

- [ ] Table created successfully
- [ ] All activity types documented
- [ ] GIN index on metadata created
- [ ] Foreign key exists

---

### Step 6: Create Assignments Table (20 minutes)

**Objective**: Track lead ownership and SLA compliance

**SQL Command**:

```sql
-- ================================================
-- 4. ASSIGNMENTS TABLE (Owner & SLA Tracking)
-- ================================================
CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID NOT NULL,
    assigned_at TIMESTAMP DEFAULT NOW(),
    
    -- Assignment Details
    owner_id VARCHAR(255) NOT NULL, -- User ID or system identifier
    owner_name VARCHAR(255),
    
    -- SLA Tracking
    sla_deadline TIMESTAMP NOT NULL,
    sla_met BOOLEAN,
    response_time_minutes INTEGER,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active', -- active, completed, reassigned
    completed_at TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_assignments_lead FOREIGN KEY (lead_id) 
        REFERENCES leads(id) ON DELETE CASCADE
);

-- Indexes for assignments table
CREATE INDEX idx_assignments_lead_id ON assignments(lead_id);
CREATE INDEX idx_assignments_owner_id ON assignments(owner_id);
CREATE INDEX idx_assignments_sla_deadline ON assignments(sla_deadline);
CREATE INDEX idx_assignments_status ON assignments(status);

COMMENT ON TABLE assignments IS 'Tracks lead ownership and SLA compliance';
```

**Field Explanations**:
- `owner_id`: ID of person assigned to lead
- `owner_name`: Name for display
- `sla_deadline`: When response is due
- `sla_met`: Whether SLA was met (calculated)
- `response_time_minutes`: How long it took to respond
- `status`: active, completed, reassigned

**Verification**:
- [ ] Table created successfully
- [ ] SLA fields present
- [ ] Indexes created

---

### Step 7: Create SLA Checking Trigger (15 minutes)

**Objective**: Automatically calculate SLA compliance when assignment is completed

**SQL Command**:

```sql
-- Trigger to check SLA on completion
CREATE OR REPLACE FUNCTION check_sla_met()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.completed_at IS NOT NULL AND OLD.completed_at IS NULL THEN
        NEW.sla_met = (NEW.completed_at <= NEW.sla_deadline);
        NEW.response_time_minutes = EXTRACT(EPOCH FROM (NEW.completed_at - NEW.assigned_at)) / 60;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_sla
BEFORE UPDATE ON assignments
FOR EACH ROW
EXECUTE FUNCTION check_sla_met();
```

**How it Works**:
1. Trigger fires BEFORE UPDATE on assignments table
2. If `completed_at` is being set (from NULL to a value)
3. Calculates if SLA was met by comparing completed_at with sla_deadline
4. Calculates response time in minutes

**Verification**:
```sql
-- Check trigger exists
SELECT trigger_name, event_manipulation, event_object_table 
FROM information_schema.triggers 
WHERE event_object_table = 'assignments';
```

- [ ] Trigger function created
- [ ] Trigger attached to assignments table

---

### Step 8: Create Database Functions (30 minutes)

**Objective**: Create utility functions for complex queries

**Function 1: Get Complete Lead Data**

```sql
-- Function to get complete lead data with all activities
CREATE OR REPLACE FUNCTION get_lead_full(lead_uuid UUID)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT json_build_object(
    'lead', row_to_json(l.*),
    'products', (
      SELECT json_agg(lp.*) 
      FROM lead_products lp 
      WHERE lp.lead_id = lead_uuid
    ),
    'current_assignment', (
      SELECT row_to_json(a.*) 
      FROM assignments a 
      WHERE a.lead_id = lead_uuid 
        AND a.status = 'active' 
      LIMIT 1
    ),
    'ai_analysis', (
      SELECT metadata
      FROM lead_activity 
      WHERE lead_id = lead_uuid 
        AND type = 'ai_result'
      ORDER BY created_at DESC
      LIMIT 1
    ),
    'activities', (
      SELECT json_agg(la.* ORDER BY la.created_at DESC) 
      FROM lead_activity la 
      WHERE la.lead_id = lead_uuid
    ),
    'pending_follow_ups', (
      SELECT json_agg(la.*) 
      FROM lead_activity la 
      WHERE la.lead_id = lead_uuid 
        AND la.type = 'follow_up'
        AND la.status = 'pending'
      ORDER BY (metadata->>'scheduled_for')::timestamp ASC
    ),
    'pending_approvals', (
      SELECT json_agg(la.*) 
      FROM lead_activity la 
      WHERE la.lead_id = lead_uuid 
        AND la.type = 'approval'
        AND la.status = 'pending'
      ORDER BY created_at DESC
    )
  ) INTO result
  FROM leads l
  WHERE l.id = lead_uuid;
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;
```

**Function 2: Get Dashboard Statistics**

```sql
-- Function to get dashboard statistics
CREATE OR REPLACE FUNCTION get_dashboard_stats()
RETURNS JSON AS $$
BEGIN
  RETURN json_build_object(
    'total_leads', (SELECT COUNT(*) FROM leads),
    'new_leads_today', (
      SELECT COUNT(*) 
      FROM leads 
      WHERE created_at::date = CURRENT_DATE
    ),
    'pending_follow_ups', (
      SELECT COUNT(*) 
      FROM lead_activity 
      WHERE type = 'follow_up' 
        AND status = 'pending'
        AND (metadata->>'scheduled_for')::timestamp <= NOW() + INTERVAL '1 hour'
    ),
    'pending_approvals', (
      SELECT COUNT(*) 
      FROM lead_activity 
      WHERE type = 'approval' 
        AND status = 'pending'
    ),
    'sla_violations', (
      SELECT COUNT(*) 
      FROM assignments 
      WHERE status = 'active' 
        AND sla_deadline < NOW()
    ),
    'avg_response_time_minutes', (
      SELECT ROUND(AVG(response_time_minutes), 0)
      FROM assignments
      WHERE completed_at IS NOT NULL
        AND completed_at > NOW() - INTERVAL '30 days'
    ),
    'conversion_rate', (
      SELECT ROUND(
        (COUNT(*) FILTER (WHERE status = 'converted')::numeric / 
         NULLIF(COUNT(*), 0) * 100), 2
      )
      FROM leads
      WHERE created_at > NOW() - INTERVAL '30 days'
    )
  );
END;
$$ LANGUAGE plpgsql;
```

**Function 3: Get Pending Follow-ups**

```sql
-- Function to get pending follow-ups
CREATE OR REPLACE FUNCTION get_pending_follow_ups()
RETURNS TABLE (
  activity_id UUID,
  lead_id UUID,
  lead_name VARCHAR,
  action VARCHAR,
  scheduled_for TIMESTAMP,
  message TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    la.id,
    la.lead_id,
    l.name,
    (la.metadata->>'action')::VARCHAR,
    (la.metadata->>'scheduled_for')::TIMESTAMP,
    la.message
  FROM lead_activity la
  JOIN leads l ON l.id = la.lead_id
  WHERE la.type = 'follow_up'
    AND la.status = 'pending'
    AND (la.metadata->>'scheduled_for')::TIMESTAMP <= NOW()
  ORDER BY (la.metadata->>'scheduled_for')::TIMESTAMP ASC;
END;
$$ LANGUAGE plpgsql;
```

**Verification**:
```sql
-- Test get_dashboard_stats
SELECT get_dashboard_stats();

-- Should return JSON with stats (all zeros since no data yet)
```

- [ ] All 3 functions created
- [ ] Functions return valid JSON
- [ ] No SQL errors

---

### Step 9: Configure Row Level Security (RLS) (25 minutes)

**Objective**: Secure database with proper access controls

**Enable RLS on all tables**:

```sql
-- Enable RLS on all tables
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;
```

**Create RLS Policies**:

```sql
-- ============================================
-- LEADS POLICIES
-- ============================================

-- Anyone can submit leads (anon users from website form)
CREATE POLICY "Anyone can submit leads"
ON leads FOR INSERT
TO anon
WITH CHECK (true);

-- Authenticated users can view leads
CREATE POLICY "Authenticated users can view leads"
ON leads FOR SELECT
TO authenticated
USING (true);

-- Authenticated users can update leads
CREATE POLICY "Authenticated users can update leads"
ON leads FOR UPDATE
TO authenticated
USING (true);

-- ============================================
-- LEAD PRODUCTS POLICIES
-- ============================================

-- Anyone can add lead products
CREATE POLICY "Anyone can add lead products"
ON lead_products FOR INSERT
TO anon
WITH CHECK (true);

-- Authenticated users can view lead products
CREATE POLICY "Authenticated users can view lead products"
ON lead_products FOR SELECT
TO authenticated
USING (true);

-- ============================================
-- LEAD ACTIVITY POLICIES
-- ============================================

-- System can log activity (both anon and authenticated)
CREATE POLICY "System can log activity"
ON lead_activity FOR INSERT
TO anon, authenticated
WITH CHECK (true);

-- Authenticated users can view activity
CREATE POLICY "Authenticated users can view activity"
ON lead_activity FOR SELECT
TO authenticated
USING (true);

-- Authenticated users can update activity status (for approvals, follow-ups)
CREATE POLICY "Authenticated users can update activity status"
ON lead_activity FOR UPDATE
TO authenticated
USING (true);

-- ============================================
-- ASSIGNMENTS POLICIES
-- ============================================

-- System can create assignments
CREATE POLICY "System can create assignments"
ON assignments FOR INSERT
TO anon, authenticated
WITH CHECK (true);

-- Authenticated users can view assignments
CREATE POLICY "Authenticated users can view assignments"
ON assignments FOR SELECT
TO authenticated
USING (true);

-- Authenticated users can update assignments
CREATE POLICY "Authenticated users can update assignments"
ON assignments FOR UPDATE
TO authenticated
USING (true);
```

**RLS Policy Explanations**:
- **anon**: Unauthenticated users (website visitors)
- **authenticated**: Logged-in admin users
- Anonymous users can submit leads and products (website form)
- Only authenticated users can view/update data
- System can log activities regardless of auth status

**Verification**:
```sql
-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('leads', 'lead_products', 'lead_activity', 'assignments');

-- Check policies
SELECT tablename, policyname, roles
FROM pg_policies
WHERE schemaname = 'public';
```

- [ ] RLS enabled on all tables
- [ ] All policies created
- [ ] Anon users can INSERT leads
- [ ] Authenticated users can SELECT/UPDATE

---

### Step 10: Insert Sample Data for Testing (20 minutes)

**Objective**: Add realistic test data to verify database works

**Sample Lead**:

```sql
-- Insert sample lead
INSERT INTO leads (
    id, name, email, phone, role, location, 
    message, status, source
)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'Priya Sharma',
    'priya.sharma@example.com',
    '+91 9876543210',
    'Architect',
    'Mumbai',
    'Looking for premium flooring options for luxury apartment project',
    'new',
    'website_form'
);

-- Insert sample products
INSERT INTO lead_products (lead_id, category, product, quantity)
VALUES 
    ('a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p', 'Flooring', 'Premium Laminate Flooring', '2000 sq ft'),
    ('a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p', 'Wall', 'Designer Wall Panels', '500 sq ft');

-- Insert AI analysis activity
INSERT INTO lead_activity (lead_id, type, status, message, actor_type, metadata)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'ai_result',
    'completed',
    'AI analyzed lead and suggested priority action',
    'ai',
    '{
        "intent": "quote_request",
        "lead_type": "architect",
        "priority": "high",
        "suggested_action": "call_within_30_min",
        "reasoning": "High-value commercial project with specific product requirements",
        "model": "llama-3.1-70b-versatile",
        "prompt_version": "v1.0"
    }'
);

-- Insert assignment
INSERT INTO assignments (lead_id, owner_id, owner_name, sla_deadline)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'sales_user_5',
    'Neha Patel',
    NOW() + INTERVAL '1 hour'
);

-- Insert assignment activity
INSERT INTO lead_activity (lead_id, type, status, message, actor_type, metadata)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'assignment',
    'completed',
    'Lead auto-assigned to Neha Patel',
    'system',
    jsonb_build_object(
        'assigned_by', 'system',
        'owner_id', 'sales_user_5',
        'owner_name', 'Neha Patel',
        'sla_deadline', (NOW() + INTERVAL '1 hour')::text
    )
);

-- Insert pending follow-up
INSERT INTO lead_activity (lead_id, type, status, message, metadata)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'follow_up',
    'pending',
    'Sales call follow-up scheduled',
    jsonb_build_object(
        'action', 'call',
        'scheduled_for', (NOW() + INTERVAL '30 minutes')::text,
        'reason', 'high_priority_lead'
    )
);
```

**Verification Queries**:

```sql
-- Check all data inserted
SELECT COUNT(*) as lead_count FROM leads;
SELECT COUNT(*) as products_count FROM lead_products;
SELECT COUNT(*) as activities_count FROM lead_activity;
SELECT COUNT(*) as assignments_count FROM assignments;

-- Test get_lead_full function with sample data
SELECT get_lead_full('a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p');

-- Test dashboard stats
SELECT get_dashboard_stats();

-- Test pending follow-ups
SELECT * FROM get_pending_follow_ups();
```

- [ ] Sample lead inserted
- [ ] Products inserted
- [ ] Activities logged
- [ ] Assignment created
- [ ] All queries return data
- [ ] Functions work with real data

---

## DAY 4: Backend Models & Database Utilities

### Step 11: Create Pydantic Models - Lead Models (30 minutes)

**Objective**: Create Pydantic models for type safety and validation

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\models\lead.py`

```python
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
```

**Key Features**:
- Email validation with `EmailStr`
- Field constraints (min/max length)
- Optional fields properly typed
- Separation of Create/Update/Read models
- Composite model for lead + products

**Verification**:
```powershell
# Navigate to backend directory
cd b:\Project\SaaS\Second\lead-automation-backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Test import
python -c "from app.models.lead import Lead, LeadSubmission; print('Models imported successfully')"
```

- [ ] File created
- [ ] Models import without errors
- [ ] All fields properly typed

---

### Step 12: Create Pydantic Models - Activity Models (25 minutes)

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\models\activity.py`

```python
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
# SPECIFIC ACTIVITY TYPES
# ============================================

class AIResultActivity(BaseModel):
    """AI analysis result metadata"""
    intent: str
    lead_type: str
    priority: str  # low, medium, high
    suggested_action: str
    reasoning: Optional[str] = None
    model: str
    prompt_version: str


class FollowUpActivity(BaseModel):
    """Follow-up activity metadata"""
    action: str  # call, email, meeting
    scheduled_for: datetime
    reason: Optional[str] = None


class ApprovalActivity(BaseModel):
    """Approval request metadata"""
    approval_type: str
    ai_recommendation: Optional[str] = None
    requires_manager: bool = False


class EmailActivity(BaseModel):
    """Email activity metadata"""
    template: str
    channel: str = "resend"
    resend_id: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0
```

**Verification**:
```powershell
python -c "from app.models.activity import LeadActivity, AIResultActivity; print('Activity models imported')"
```

- [ ] Activity models created
- [ ] Specific activity type models defined
- [ ] Imports successful

---

### Step 13: Create Pydantic Models - Assignment Models (20 minutes)

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\models\assignment.py`

```python
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
```

**Verification**:
```powershell
python -c "from app.models.assignment import Assignment; print('Assignment models imported')"
```

- [ ] Assignment models created
- [ ] SLA fields included
- [ ] Imports successful

---

### Step 14: Create Database Utility Functions (30 minutes)

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\utils\db.py`

```python
from supabase import create_client, Client
from app.config import settings
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# ============================================
# SUPABASE CLIENT
# ============================================

# Initialize Supabase client with service key for backend operations
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY  # Use service key for backend
)


# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

async def execute_rpc(function_name: str, params: Optional[Dict] = None) -> Any:
    """
    Execute a Supabase RPC (Remote Procedure Call) function
    
    Args:
        function_name: Name of the PostgreSQL function
        params: Optional parameters dictionary
        
    Returns:
        Function result
    """
    try:
        result = supabase.rpc(function_name, params or {}).execute()
        return result.data
    except Exception as e:
        logger.error(f"RPC call to {function_name} failed: {str(e)}")
        raise


async def get_lead_full(lead_id: str) -> Dict[str, Any]:
    """
    Get complete lead data including products, activities, assignments
    
    Args:
        lead_id: UUID of the lead
        
    Returns:
        Complete lead data as dictionary
    """
    return await execute_rpc("get_lead_full", {"lead_uuid": lead_id})


async def get_dashboard_stats() -> Dict[str, Any]:
    """
    Get dashboard statistics
    
    Returns:
        Dashboard metrics dictionary
    """
    return await execute_rpc("get_dashboard_stats")


async def get_pending_follow_ups() -> List[Dict[str, Any]]:
    """
    Get all pending follow-ups that are due
    
    Returns:
        List of pending follow-ups
    """
    return await execute_rpc("get_pending_follow_ups")


# ============================================
# CRUD HELPERS
# ============================================

async def insert_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a record into a table
    
    Args:
        table: Table name
        data: Data dict to insert
        
    Returns:
        Inserted record
    """
    try:
        result = supabase.table(table).insert(data).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        logger.error(f"Insert into {table} failed: {str(e)}")
        raise


async def update_record(
    table: str, 
    record_id: str, 
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a record in a table
    
    Args:
        table: Table name
        record_id: UUID of record to update
        data: Data dict to update
        
    Returns:
        Updated record
    """
    try:
        result = supabase.table(table).update(data).eq("id", record_id).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        logger.error(f"Update {table} record {record_id} failed: {str(e)}")
        raise


async def get_record(table: str, record_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a single record by ID
    
    Args:
        table: Table name
        record_id: UUID of record
        
    Returns:
        Record dict or None
    """
    try:
        result = supabase.table(table).select("*").eq("id", record_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Get {table} record {record_id} failed: {str(e)}")
        return None


async def query_records(
    table: str, 
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Query records from a table with filters
    
    Args:
        table: Table name
        filters: Dictionary of column: value filters
        order_by: Column to order by
        limit: Max number of records
        
    Returns:
        List of records
    """
    try:
        query = supabase.table(table).select("*")
        
        # Apply filters
        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)
        
        # Apply ordering
        if order_by:
            query = query.order(order_by)
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        result = query.execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Query {table} failed: {str(e)}")
        return []
```

**Key Features**:
- Supabase client initialization with service key
- RPC function wrappers for database functions
- Generic CRUD helpers
- Error handling and logging
- Type hints for better IDE support

**Verification**:
```powershell
# Test database connection
python -c "from app.utils.db import supabase; print('DB client initialized:', supabase)"
```

- [ ] Database utility file created
- [ ] Supabase client initializes
- [ ] Helper functions defined
- [ ] No import errors

---

### Step 15: Test Database Connection from Backend (20 minutes)

**Objective**: Verify backend can connect to Supabase and query data

**Create Test Script**: `b:\Project\SaaS\Second\lead-automation-backend\test_db.py`

```python
import asyncio
from app.utils.db import (
    get_dashboard_stats,
    get_pending_follow_ups,
    get_lead_full,
    query_records
)

async def test_database_connection():
    """Test database connection and basic queries"""
    print("=== Testing Database Connection ===\n")
    
    # Test 1: Dashboard stats
    print("1. Testing get_dashboard_stats()...")
    try:
        stats = await get_dashboard_stats()
        print(f"✅ Dashboard Stats: {stats}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test 2: Query leads
    print("2. Testing query_records (leads)...")
    try:
        leads = await query_records("leads", limit=5)
        print(f"✅ Found {len(leads)} leads")
        if leads:
            print(f"   First lead: {leads[0]['name']} ({leads[0]['email']})\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test 3: Get full lead data (if sample data exists)
    if leads:
        lead_id = leads[0]['id']
        print(f"3. Testing get_lead_full() for lead {lead_id}...")
        try:
            full_lead = await get_lead_full(lead_id)
            print(f"✅ Full lead data retrieved")
            print(f"   Products: {len(full_lead.get('products', []))}")
            print(f"   Activities: {len(full_lead.get('activities', []))}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    # Test 4: Pending follow-ups
    print("4. Testing get_pending_follow_ups()...")
    try:
        follow_ups = await get_pending_follow_ups()
        print(f"✅ Found {len(follow_ups)} pending follow-ups\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    print("=== All Tests Complete ===")

if __name__ == "__main__":
    asyncio.run(test_database_connection())
```

**Run Tests**:

```powershell
# Make sure you're in backend directory with venv activated
cd b:\Project\SaaS\Second\lead-automation-backend
.\venv\Scripts\Activate.ps1

# Run test script
python test_db.py
```

**Expected Output**:
```
=== Testing Database Connection ===

1. Testing get_dashboard_stats()...
✅ Dashboard Stats: {'total_leads': 1, 'new_leads_today': 1, ...}

2. Testing query_records (leads)...
✅ Found 1 leads
   First lead: Priya Sharma (priya.sharma@example.com)

3. Testing get_lead_full() for lead ...
✅ Full lead data retrieved
   Products: 2
   Activities: 3

4. Testing get_pending_follow_ups()...
✅ Found 1 pending follow-ups

=== All Tests Complete ===
```

**Verification**:
- [ ] All tests pass
- [ ] Dashboard stats return numbers
- [ ] Sample lead is retrieved
- [ ] Full lead data includes products and activities
- [ ] No connection errors

---

### Step 16: Update Backend Health Check with Database Status (15 minutes)

**Objective**: Add database health check to the backend API

**File**: `b:\Project\SaaS\Second\lead-automation-backend\app\main.py`

Update the health check endpoint:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.db import supabase, get_dashboard_stats

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-Powered Lead Management Automation System",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    """Detailed health check endpoint with database status"""
    
    # Test database connection
    db_status = "operational"
    try:
        # Try to query dashboard stats
        stats = await get_dashboard_stats()
        db_connected = True
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_connected = False
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "services": {
            "api": "operational",
            "database": db_status,
            "supabase": "operational" if db_connected else "error",
            "groq": "pending",      # Will test in Phase 4
            "resend": "pending"     # Will test in Phase 4
        },
        "database_stats": stats if db_connected else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Auto-reload on code changes
    )
```

**Test Updated Health Check**:

```powershell
# Start backend (if not running)
cd b:\Project\SaaS\Second\lead-automation-backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000/health

**Expected Response**:
```json
{
  "status": "healthy",
  "services": {
    "api": "operational",
    "database": "operational",
    "supabase": "operational",
    "groq": "pending",
    "resend": "pending"
  },
  "database_stats": {
    "total_leads": 1,
    "new_leads_today": 1,
    "pending_follow_ups": 1,
    ...
  }
}
```

**Verification**:
- [ ] Backend starts without errors
- [ ] /health endpoint returns database stats
- [ ] Database status shows "operational"
- [ ] Frontend health check shows database connected

---

## 📊 Phase 3 Completion Checklist

### Database Schema
- [ ] All 4 tables created (leads, lead_products, lead_activity, assignments)
- [ ] Foreign key constraints in place
- [ ] Indexes created for performance
- [ ] Row Level Security (RLS) enabled and policies configured
- [ ] Database functions created (get_lead_full, get_dashboard_stats, get_pending_follow_ups)
- [ ] SLA checking trigger created and tested
- [ ] Sample data inserted successfully

### Backend Models
- [ ] Lead models created (LeadBase, LeadCreate, Lead, etc.)
- [ ] Activity models created (LeadActivity, AIResultActivity, etc.)
- [ ] Assignment models created
- [ ] All models validate correctly

### Database Utilities
- [ ] Supabase client initialized
- [ ] RPC function wrappers created
- [ ] CRUD helper functions implemented
- [ ] Error handling in place
- [ ] Test script runs successfully

### Integration
- [ ] Backend can connect to database
- [ ] Health check shows database status
- [ ] Dashboard stats endpoint works
- [ ] Can query leads, products, activities
- [ ] Event-sourcing pattern verified

---

## 🎯 Success Metrics

**Database Performance**:
- All queries run in < 100ms for sample data
- Indexes are used (verify with EXPLAIN ANALYZE)
- RLS policies don't significantly impact performance

**Code Quality**:
- All models have proper type hints
- Database functions have error handling
- No SQL injection vulnerabilities (using parameterized queries)

**Functionality**:
- Can create leads with products
- Can log activities with metadata
- Can query full lead data
- Dashboard stats calculate correctly
- Follow-ups and approvals stored as activities

---

## 🔍 Troubleshooting

### Common Issues

**Issue 1: Cannot connect to Supabase**
```
Error: Invalid Supabase credentials
```
**Solution**: 
- Check `.env` file has correct SUPABASE_URL and SUPABASE_SERVICE_KEY
- Verify keys are not wrapped in quotes
- Restart backend after updating .env

**Issue 2: RLS blocks queries**
```
Error: permission denied for table leads
```
**Solution**:
- Ensure you're using SUPABASE_SERVICE_KEY (not ANON_KEY) in backend
- Service key bypasses RLS
- Check RLS policies allow the operation

**Issue 3: Functions not found**
```
Error: function get_lead_full does not exist
```
**Solution**:
- Re-run the function creation SQL
- Check function was created in correct schema (public)
- Verify with: `SELECT * FROM pg_proc WHERE proname = 'get_lead_full';`

**Issue 4: Trigger not firing**
```
SLA fields not calculated
```
**Solution**:
- Verify trigger exists: `SELECT * FROM pg_trigger WHERE tgname = 'trigger_check_sla';`
- Check trigger function has no errors
- Test by updating assignment with completed_at timestamp

---

## 📚 Additional Resources

### Supabase Documentation
- [Supabase SQL Editor](https://supabase.com/docs/guides/database/overview)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Database Functions](https://supabase.com/docs/guides/database/functions)

### Pydantic Documentation
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)
- [Field Validation](https://docs.pydantic.dev/latest/concepts/validation/)

### PostgreSQL Resources
- [JSONB Data Type](https://www.postgresql.org/docs/current/datatype-json.html)
- [GIN Indexes](https://www.postgresql.org/docs/current/gin.html)
- [Triggers](https://www.postgresql.org/docs/current/triggers.html)

---

## 🎉 Phase 3 Complete!

Once all steps are verified:

✅ **Database**: 4 tables with proper relationships  
✅ **Security**: RLS policies protecting data  
✅ **Performance**: Indexes for fast queries  
✅ **Functions**: Complex queries simplified  
✅ **Models**: Type-safe Pydantic models  
✅ **Utilities**: Backend-database communication ready  
✅ **Testing**: Sample data and verification complete  

**You're now ready for Phase 4: Backend API Development!** 🚀

---

## 📝 Notes

- Event-sourcing pattern is implemented via `lead_activity` table
- AI results are NEVER stored in `leads` table
- All AI outputs include model version and prompt version for auditability
- Follow-ups and approvals are activities, not separate tables
- SLA tracking is automatic via triggers
- Database functions reduce API complexity

**Next Phase Preview**: Phase 4 will implement the FastAPI endpoints to create leads, log activities, manage assignments, and provide analytics using these database structures.
