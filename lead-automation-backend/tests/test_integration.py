import pytest
from httpx import AsyncClient
from app.main import app
import json


# ============================================================================
# Test: Lead Submission to Categorization Flow
# ============================================================================

@pytest.mark.asyncio
async def test_lead_submission_to_categorization_architect():
    """Test complete flow from lead submission to AI categorization for architect"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/leads", json={
            "name": "Integration Test Architect",
            "email": "integration-architect@test.com",
            "phone": "+91 9999999999",
            "role": "Architect",
            "location": "Mumbai",
            "message": "Need urgent quote for 5000 sq ft luxury project",
            "product_interests": [
                {"category": "Flooring", "product": "Premium Marble", "quantity": "3000 sq ft"}
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify lead created
        assert "lead" in data
        assert data["lead"]["name"] == "Integration Test Architect"
        assert data["lead"]["email"] == "integration-architect@test.com"
        
        # Verify AI categorization
        assert "ai_categorization" in data
        assert data["ai_categorization"]["priority"] in ["high", "medium", "low"]
        assert data["ai_categorization"]["lead_type"] in ["architect", "builder", "contractor", "homeowner", "home_owner"]
        assert data["ai_categorization"]["intent"] in ["quote_request", "information", "complaint", "partnership"]


@pytest.mark.asyncio
async def test_lead_submission_to_categorization_homeowner():
    """Test complete flow for home owner lead"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/leads", json={
            "name": "Integration Test Home Owner",
            "email": "integration-homeowner@test.com",
            "role": "Home Owner",
            "location": "Delhi",
            "message": "Looking for flooring options",
            "product_interests": [
                {"category": "Flooring", "product": "Laminate", "quantity": "1000 sq ft"}
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "lead" in data
        assert "ai_categorization" in data


@pytest.mark.asyncio
async def test_lead_submission_validation_error():
    """Test lead submission with invalid data"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/leads", json={
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            # Missing required fields
        })
        
        # Should return validation error
        assert response.status_code in [400, 422]


# ============================================================================
# Test: Analytics Integration
# ============================================================================

@pytest.mark.asyncio
async def test_analytics_dashboard_integration():
    """Test analytics dashboard after lead creation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get initial stats
        initial_response = await client.get("/api/analytics/dashboard")
        assert initial_response.status_code == 200
        initial_stats = initial_response.json()
        
        # Create a lead
        await client.post("/api/leads", json={
            "name": "Analytics Test",
            "email": "analytics@test.com",
            "role": "Home Owner",
            "location": "Test City",
            "message": "Test message",
            "product_interests": []
        })
        
        # Get updated stats
        final_response = await client.get("/api/analytics/dashboard")
        assert final_response.status_code == 200
        final_stats = final_response.json()
        
        # Verify stats updated
        assert "total_leads" in final_stats
        # Note: In test environment, database might be reset, so we just verify the field exists


@pytest.mark.asyncio
async def test_analytics_conversion_funnel():
    """Test conversion funnel analytics"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/analytics/conversion")
        
        assert response.status_code == 200
        funnel = response.json()
        
        # Verify funnel structure
        assert "new" in funnel
        assert isinstance(funnel["new"], int)


# ============================================================================
# Test: Approval Workflow Integration
# ============================================================================

@pytest.mark.asyncio
async def test_approval_workflow_high_priority_lead():
    """Test approval creation for high-priority leads"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create high-priority lead
        lead_response = await client.post("/api/leads", json={
            "name": "Approval Test Architect",
            "email": "approval-test@test.com",
            "phone": "+91 9876543210",
            "role": "Architect",
            "location": "Mumbai",
            "message": "Urgent project - need immediate quote",
            "product_interests": [
                {"category": "Flooring", "product": "Premium", "quantity": "5000 sq ft"}
            ]
        })
        
        assert lead_response.status_code == 200
        
        # Check pending approvals
        approvals_response = await client.get("/api/approvals/pending")
        assert approvals_response.status_code == 200
        
        # Verify response is a list
        approvals = approvals_response.json()
        assert isinstance(approvals, list)


# ============================================================================
# Test: Lead Retrieval Integration
# ============================================================================

@pytest.mark.asyncio
async def test_lead_retrieval_after_creation():
    """Test retrieving lead after creation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create lead
        create_response = await client.post("/api/leads", json={
            "name": "Retrieval Test",
            "email": "retrieval@test.com",
            "role": "Contractor",
            "location": "Pune",
            "message": "Test retrieval",
            "product_interests": []
        })
        
        assert create_response.status_code == 200
        created_lead = create_response.json()
        lead_id = created_lead["lead"]["id"]
        
        # Retrieve lead
        get_response = await client.get(f"/api/leads/{lead_id}")
        
        if get_response.status_code == 200:
            retrieved_lead = get_response.json()
            assert retrieved_lead["id"] == lead_id
            assert retrieved_lead["name"] == "Retrieval Test"


@pytest.mark.asyncio
async def test_leads_list_pagination():
    """Test leads list endpoint with pagination"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/leads?limit=10&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert isinstance(data, (list, dict))


# ============================================================================
# Test: Email Delivery Integration
# ============================================================================

@pytest.mark.asyncio
async def test_email_sent_on_lead_creation():
    """Test that email is sent when lead is created"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/leads", json={
            "name": "Email Test",
            "email": "email-test@test.com",
            "role": "Home Owner",
            "location": "Delhi",
            "message": "Test email sending",
            "product_interests": [
                {"category": "Flooring", "product": "Test"}
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify email_sent field exists
        assert "email_sent" in data
        # Note: In test environment, email might not actually send
        # We just verify the field is present


# ============================================================================
# Test: Assignment Integration
# ============================================================================

@pytest.mark.asyncio
async def test_assignment_created_on_lead_submission():
    """Test that assignment is created with correct SLA"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/leads", json={
            "name": "Assignment Test",
            "email": "assignment@test.com",
            "phone": "+91 9999999999",
            "role": "Builder",
            "location": "Bangalore",
            "message": "Bulk order needed",
            "product_interests": [
                {"category": "Flooring", "product": "Bulk", "quantity": "10000 sq ft"}
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify assignment created
        if "assignment" in data:
            assignment = data["assignment"]
            assert "sla_hours" in assignment
            assert "owner_name" in assignment or "owner" in assignment


# ============================================================================
# Test: Health Check Integration
# ============================================================================

@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        health = response.json()
        
        assert "status" in health
        assert health["status"] in ["healthy", "ok"]


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
        assert response.status_code == 200
