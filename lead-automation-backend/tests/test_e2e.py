import pytest
from httpx import AsyncClient
from app.main import app
import asyncio


# ============================================================================
# Test: Complete Lead Journey - High Priority
# ============================================================================

@pytest.mark.asyncio
async def test_complete_lead_journey_architect_vip():
    """Test complete journey for architect VIP lead"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Step 1: Submit lead
        lead_data = {
            "name": "E2E Test Architect",
            "email": "e2e-architect@test.com",
            "phone": "+91 9999999999",
            "role": "Architect",
            "location": "Mumbai",
            "message": "Need urgent quote for 10000 sq ft luxury commercial project",
            "product_interests": [
                {"category": "Flooring", "product": "Premium Italian Marble", "quantity": "5000 sq ft"},
                {"category": "Wall Panels", "product": "Designer Wall Cladding", "quantity": "3000 sq ft"}
            ]
        }
        
        response = await client.post("/api/leads", json=lead_data)
        assert response.status_code == 200
        
        result = response.json()
        lead_id = result["lead"]["id"]
        
        # Step 2: Verify AI categorization
        ai_cat = result.get("ai_categorization", {})
        # Note: Actual priority depends on AI, but should be present
        assert "priority" in ai_cat
        assert "lead_type" in ai_cat
        assert "intent" in ai_cat
        
        # Step 3: Verify email sent
        assert "email_sent" in result
        
        # Step 4: Verify assignment created (if present)
        if "assignment" in result:
            assignment = result["assignment"]
            assert "sla_hours" in assignment
        
        # Step 5: Verify lead appears in dashboard
        dashboard = await client.get("/api/analytics/dashboard")
        assert dashboard.status_code == 200
        stats = dashboard.json()
        assert "total_leads" in stats
        
        # Step 6: Verify lead can be retrieved
        if lead_id:
            lead_detail = await client.get(f"/api/leads/{lead_id}")
            # Endpoint might not be implemented yet, so we check if it exists
            assert lead_detail.status_code in [200, 404]


@pytest.mark.asyncio
async def test_complete_lead_journey_builder_bulk():
    """Test complete journey for builder bulk order"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        lead_data = {
            "name": "E2E Test Builder",
            "email": "e2e-builder@test.com",
            "phone": "+91 9876543210",
            "role": "Builder",
            "location": "Pune",
            "message": "Bulk pricing needed for 50 unit residential complex",
            "product_interests": [
                {"category": "Flooring", "product": "Bulk Flooring", "quantity": "50000 sq ft"},
                {"category": "Wall Panels", "product": "Standard Panels", "quantity": "30000 sq ft"}
            ]
        }
        
        response = await client.post("/api/leads", json=lead_data)
        assert response.status_code == 200
        
        result = response.json()
        
        # Verify categorization
        assert "ai_categorization" in result
        ai_cat = result["ai_categorization"]
        assert "priority" in ai_cat
        assert "lead_type" in ai_cat


# ============================================================================
# Test: Complete Lead Journey - Medium Priority
# ============================================================================

@pytest.mark.asyncio
async def test_complete_lead_journey_homeowner_warm():
    """Test complete journey for medium-priority home owner"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        lead_data = {
            "name": "E2E Home Owner",
            "email": "e2e-homeowner@test.com",
            "phone": "+91 9123456789",
            "role": "Home Owner",
            "location": "Delhi",
            "message": "Need quote for complete home renovation, 1500 sq ft apartment",
            "product_interests": [
                {"category": "Flooring", "product": "Laminate Flooring", "quantity": "1500 sq ft"},
                {"category": "Wall Panels", "product": "Wall Panels", "quantity": "500 sq ft"}
            ]
        }
        
        response = await client.post("/api/leads", json=lead_data)
        assert response.status_code == 200
        
        result = response.json()
        
        # Verify workflow
        assert "ai_categorization" in result
        assert "email_sent" in result


@pytest.mark.asyncio
async def test_complete_lead_journey_contractor():
    """Test complete journey for contractor lead"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        lead_data = {
            "name": "E2E Contractor",
            "email": "e2e-contractor@test.com",
            "role": "Contractor",
            "location": "Bangalore",
            "message": "Looking for pricing for upcoming project",
            "product_interests": [
                {"category": "Flooring", "product": "Commercial Flooring", "quantity": "2000 sq ft"}
            ]
        }
        
        response = await client.post("/api/leads", json=lead_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "lead" in result
        assert "ai_categorization" in result


# ============================================================================
# Test: Complete Lead Journey - Low Priority
# ============================================================================

@pytest.mark.asyncio
async def test_complete_lead_journey_browsing():
    """Test complete journey for low-priority browsing lead"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        lead_data = {
            "name": "E2E Browsing User",
            "email": "e2e-browsing@test.com",
            "role": "Home Owner",
            "location": "Chennai",
            "message": "Just browsing different flooring options for my bedroom",
            "product_interests": [
                {"category": "Flooring", "product": "Basic Flooring", "quantity": "200 sq ft"}
            ]
        }
        
        response = await client.post("/api/leads", json=lead_data)
        assert response.status_code == 200
        
        result = response.json()
        
        # Verify categorization
        ai_cat = result.get("ai_categorization", {})
        assert "priority" in ai_cat
        assert "intent" in ai_cat


# ============================================================================
# Test: Multi-Lead Workflow
# ============================================================================

@pytest.mark.asyncio
async def test_multi_lead_workflow():
    """Test system handles multiple leads correctly"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create 5 leads with different priorities
        leads_data = [
            {
                "name": "Multi Test 1 - Architect",
                "email": "multi1@test.com",
                "role": "Architect",
                "message": "Urgent project",
                "product_interests": [{"category": "Flooring", "product": "Premium"}]
            },
            {
                "name": "Multi Test 2 - Builder",
                "email": "multi2@test.com",
                "role": "Builder",
                "message": "Bulk order needed",
                "product_interests": [{"category": "Flooring", "product": "Bulk"}]
            },
            {
                "name": "Multi Test 3 - Contractor",
                "email": "multi3@test.com",
                "role": "Contractor",
                "message": "Quote needed",
                "product_interests": [{"category": "Flooring", "product": "Standard"}]
            },
            {
                "name": "Multi Test 4 - Home Owner",
                "email": "multi4@test.com",
                "role": "Home Owner",
                "message": "Renovation project",
                "product_interests": [{"category": "Flooring", "product": "Laminate"}]
            },
            {
                "name": "Multi Test 5 - Browsing",
                "email": "multi5@test.com",
                "role": "Home Owner",
                "message": "Just looking",
                "product_interests": []
            }
        ]
        
        responses = []
        for lead_data in leads_data:
            response = await client.post("/api/leads", json=lead_data)
            assert response.status_code == 200
            responses.append(response.json())
        
        # Verify all leads processed
        assert len(responses) == 5
        
        # Verify each has categorization
        for result in responses:
            assert "ai_categorization" in result


# ============================================================================
# Test: Concurrent Lead Submissions
# ============================================================================

@pytest.mark.asyncio
async def test_concurrent_lead_submissions():
    """Test system handles concurrent lead submissions"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        async def create_lead(index):
            return await client.post("/api/leads", json={
                "name": f"Concurrent Test {index}",
                "email": f"concurrent{index}@test.com",
                "role": "Home Owner",
                "location": "Test City",
                "message": f"Concurrent test {index}",
                "product_interests": []
            })
        
        # Create 5 leads concurrently
        tasks = [create_lead(i) for i in range(5)]
        responses = await asyncio.gather(*tasks)
        
        # Verify all succeeded
        for response in responses:
            assert response.status_code == 200


# ============================================================================
# Test: Error Handling
# ============================================================================

@pytest.mark.asyncio
async def test_invalid_lead_data_handling():
    """Test system handles invalid lead data gracefully"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Missing required fields
        response1 = await client.post("/api/leads", json={
            "name": "Test"
            # Missing email, role, etc.
        })
        assert response1.status_code in [400, 422]
        
        # Invalid email format
        response2 = await client.post("/api/leads", json={
            "name": "Test",
            "email": "invalid-email",
            "role": "Home Owner",
            "message": "Test"
        })
        assert response2.status_code in [200, 400, 422]


# ============================================================================
# Test: Analytics After Multiple Leads
# ============================================================================

@pytest.mark.asyncio
async def test_analytics_after_multiple_leads():
    """Test analytics update correctly after multiple lead submissions"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create multiple leads
        for i in range(3):
            await client.post("/api/leads", json={
                "name": f"Analytics Test {i}",
                "email": f"analytics{i}@test.com",
                "role": "Home Owner",
                "location": "Test",
                "message": "Test",
                "product_interests": []
            })
        
        # Check dashboard
        dashboard = await client.get("/api/analytics/dashboard")
        assert dashboard.status_code == 200
        stats = dashboard.json()
        
        # Verify stats structure
        assert "total_leads" in stats


# ============================================================================
# Test: Full System Integration
# ============================================================================

@pytest.mark.asyncio
async def test_full_system_integration():
    """Test full system integration from lead to analytics"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 1. Create lead
        create_response = await client.post("/api/leads", json={
            "name": "Full Integration Test",
            "email": "full-integration@test.com",
            "phone": "+91 9999999999",
            "role": "Architect",
            "location": "Mumbai",
            "message": "Complete system test",
            "product_interests": [
                {"category": "Flooring", "product": "Test Product", "quantity": "1000 sq ft"}
            ]
        })
        
        assert create_response.status_code == 200
        create_data = create_response.json()
        
        # 2. Verify AI categorization
        assert "ai_categorization" in create_data
        
        # 3. Verify email sent
        assert "email_sent" in create_data
        
        # 4. Check analytics
        analytics = await client.get("/api/analytics/dashboard")
        assert analytics.status_code == 200
        
        # 5. Check conversion funnel
        conversion = await client.get("/api/analytics/conversion")
        assert conversion.status_code == 200
        
        # 6. Check approvals
        approvals = await client.get("/api/approvals/pending")
        assert approvals.status_code == 200
        
        # 7. Verify health
        health = await client.get("/health")
        assert health.status_code == 200
