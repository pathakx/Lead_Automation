-- ================================================
-- AI Lead Management System - Database Schema
-- OPTION 2 COMPLIANT - SIMPLIFIED & AI-FIRST
-- ================================================
-- Database: PostgreSQL (Supabase)
-- Created: 2024-12-24
-- ================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

COMMENT ON TABLE leads IS 'Stores ONLY source data from form submissions. No AI-generated fields.';
COMMENT ON COLUMN leads.status IS 'Human-set status, not AI-generated';

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

-- ================================================
-- UTILITY FUNCTIONS
-- ================================================

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

-- ================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ================================================

-- Enable RLS on all tables
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;

-- Leads policies
CREATE POLICY "Anyone can submit leads"
ON leads FOR INSERT
TO anon
WITH CHECK (true);

CREATE POLICY "Authenticated users can view leads"
ON leads FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Authenticated users can update leads"
ON leads FOR UPDATE
TO authenticated
USING (true);

-- Lead products policies
CREATE POLICY "Anyone can add lead products"
ON lead_products FOR INSERT
TO anon
WITH CHECK (true);

CREATE POLICY "Authenticated users can view lead products"
ON lead_products FOR SELECT
TO authenticated
USING (true);

-- Lead activity policies (PUBLIC CAN LOG, ALL CAN VIEW)
CREATE POLICY "System can log activity"
ON lead_activity FOR INSERT
TO anon, authenticated
WITH CHECK (true);

CREATE POLICY "Authenticated users can view activity"
ON lead_activity FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Authenticated users can update activity status"
ON lead_activity FOR UPDATE
TO authenticated
USING (true);

-- Assignments policies
CREATE POLICY "System can create assignments"
ON assignments FOR INSERT
TO anon, authenticated
WITH CHECK (true);

CREATE POLICY "Authenticated users can view assignments"
ON assignments FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Authenticated users can update assignments"
ON assignments FOR UPDATE
TO authenticated
USING (true);

-- ================================================
-- SAMPLE DATA (For Testing)
-- ================================================

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
        "reasoning": "High-value commercial project with specific product requirements"
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
    '{
        "assigned_by": "system",
        "owner_id": "sales_user_5",
        "owner_name": "Neha Patel",
        "sla_deadline": "' || (NOW() + INTERVAL '1 hour')::text || '"
    }'
);

-- Insert pending follow-up
INSERT INTO lead_activity (lead_id, type, status, message, metadata)
VALUES (
    'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p',
    'follow_up',
    'pending',
    'Sales call follow-up scheduled',
    '{
        "action": "call",
        "scheduled_for": "' || (NOW() + INTERVAL '30 minutes')::text || '",
        "reason": "high_priority_lead"
    }'
);

-- ================================================
-- END OF SCHEMA
-- ================================================

-- Summary:
-- ✅ 4 core tables: leads, lead_products, lead_activity, assignments
-- ✅ AI results stored as activities (no DB pollution)
-- ✅ Follow-ups stored as activities with status='pending'
-- ✅ Approvals stored as activities with type='approval'
-- ✅ Event-sourcing pattern for full auditability
-- ✅ Clean, demo-friendly, interview-safe
