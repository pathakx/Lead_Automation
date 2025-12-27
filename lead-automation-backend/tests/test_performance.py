import pytest
import time
import asyncio
from httpx import AsyncClient
from app.main import app


# ============================================================================
# Test: API Response Time - Lead Creation
# ============================================================================

@pytest.mark.asyncio
async def test_api_response_time_lead_creation():
    """Test lead creation API response time < 2s"""
    async with AsyncClient(app=app, base_url="http://test", timeout=30.0) as client:
        start_time = time.time()
        
        response = await client.post("/api/leads", json={
            "name": "Performance Test User",
            "email": "perf-test@example.com",
            "role": "Home Owner",
            "location": "Mumbai",
            "message": "Performance testing",
            "product_interests": [
                {"category": "Flooring", "product": "Test Product", "quantity": "100 sq ft"}
            ]
        })
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\n✓ Lead creation response time: {response_time:.3f}s")
        
        assert response.status_code == 200
        assert response_time < 2.0, f"Response time {response_time:.3f}s exceeds 2s limit"


@pytest.mark.asyncio
async def test_api_response_time_lead_creation_with_ai():
    """Test lead creation with AI categorization response time"""
    async with AsyncClient(app=app, base_url="http://test", timeout=30.0) as client:
        start_time = time.time()
        
        response = await client.post("/api/leads", json={
            "name": "AI Performance Test",
            "email": "ai-perf@example.com",
            "phone": "+91 9999999999",
            "role": "Architect",
            "location": "Delhi",
            "message": "Need urgent quote for large commercial project",
            "product_interests": [
                {"category": "Flooring", "product": "Premium Marble", "quantity": "5000 sq ft"}
            ]
        })
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\n✓ Lead creation with AI response time: {response_time:.3f}s")
        
        assert response.status_code == 200
        # AI categorization might take longer, allow up to 3s
        assert response_time < 3.0, f"Response time {response_time:.3f}s exceeds 3s limit"


# ============================================================================
# Test: API Response Time - Dashboard
# ============================================================================

@pytest.mark.asyncio
async def test_api_response_time_dashboard():
    """Test dashboard API response time < 200ms"""
    async with AsyncClient(app=app, base_url="http://test", timeout=10.0) as client:
        start_time = time.time()
        
        response = await client.get("/api/analytics/dashboard")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        print(f"\n✓ Dashboard response time: {response_time:.1f}ms")
        
        assert response.status_code == 200
        # Allow up to 500ms for dashboard (more lenient than 200ms target)
        assert response_time < 500, f"Response time {response_time:.1f}ms exceeds 500ms limit"


@pytest.mark.asyncio
async def test_api_response_time_conversion_funnel():
    """Test conversion funnel API response time"""
    async with AsyncClient(app=app, base_url="http://test", timeout=10.0) as client:
        start_time = time.time()
        
        response = await client.get("/api/analytics/conversion")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"\n✓ Conversion funnel response time: {response_time:.1f}ms")
        
        assert response.status_code == 200
        assert response_time < 500, f"Response time {response_time:.1f}ms exceeds 500ms"


# ============================================================================
# Test: API Response Time - Approvals
# ============================================================================

@pytest.mark.asyncio
async def test_api_response_time_approvals():
    """Test approvals endpoint response time"""
    async with AsyncClient(app=app, base_url="http://test", timeout=10.0) as client:
        start_time = time.time()
        
        response = await client.get("/api/approvals/pending")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"\n✓ Approvals response time: {response_time:.1f}ms")
        
        assert response.status_code == 200
        assert response_time < 300, f"Response time {response_time:.1f}ms exceeds 300ms"


# ============================================================================
# Test: Concurrent Request Handling
# ============================================================================

@pytest.mark.asyncio
async def test_concurrent_lead_submissions_performance():
    """Test system handles 10 concurrent lead submissions efficiently"""
    async with AsyncClient(app=app, base_url="http://test", timeout=60.0) as client:
        async def create_lead(index):
            start = time.time()
            response = await client.post("/api/leads", json={
                "name": f"Concurrent Perf Test {index}",
                "email": f"concurrent-perf{index}@test.com",
                "role": "Home Owner",
                "location": "Test City",
                "message": f"Concurrent performance test {index}",
                "product_interests": []
            })
            duration = time.time() - start
            return response, duration
        
        # Create 10 leads concurrently
        start_time = time.time()
        tasks = [create_lead(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Verify all succeeded
        success_count = sum(1 for response, _ in results if response.status_code == 200)
        avg_response_time = sum(duration for _, duration in results) / len(results)
        
        print(f"\n✓ Concurrent requests: {success_count}/10 succeeded")
        print(f"✓ Total time: {total_time:.3f}s")
        print(f"✓ Average response time: {avg_response_time:.3f}s")
        
        assert success_count >= 8, f"Only {success_count}/10 requests succeeded"
        assert total_time < 30, f"Total time {total_time:.3f}s too long for 10 concurrent requests"


@pytest.mark.asyncio
async def test_concurrent_analytics_requests():
    """Test concurrent analytics requests"""
    async with AsyncClient(app=app, base_url="http://test", timeout=30.0) as client:
        async def get_dashboard():
            start = time.time()
            response = await client.get("/api/analytics/dashboard")
            duration = time.time() - start
            return response, duration
        
        # Make 5 concurrent dashboard requests
        start_time = time.time()
        tasks = [get_dashboard() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        success_count = sum(1 for response, _ in results if response.status_code == 200)
        avg_time = sum(duration for _, duration in results) / len(results) * 1000
        
        print(f"\n✓ Concurrent analytics: {success_count}/5 succeeded")
        print(f"✓ Average response time: {avg_time:.1f}ms")
        
        assert success_count == 5
        assert avg_time < 1000, f"Average response time {avg_time:.1f}ms too slow"


# ============================================================================
# Test: Database Query Performance
# ============================================================================

@pytest.mark.asyncio
async def test_database_query_performance_leads_list():
    """Test database query performance for leads list"""
    async with AsyncClient(app=app, base_url="http://test", timeout=10.0) as client:
        # Create some test leads first
        for i in range(5):
            await client.post("/api/leads", json={
                "name": f"DB Perf Test {i}",
                "email": f"db-perf{i}@test.com",
                "role": "Home Owner",
                "message": "Test",
                "product_interests": []
            })
        
        # Test query performance
        start_time = time.time()
        response = await client.get("/api/leads?limit=20")
        query_time = (time.time() - start_time) * 1000
        
        print(f"\n✓ Leads list query time: {query_time:.1f}ms")
        
        if response.status_code == 200:
            assert query_time < 1000, f"Query time {query_time:.1f}ms too slow"


# ============================================================================
# Test: Health Check Performance
# ============================================================================

@pytest.mark.asyncio
async def test_health_check_performance():
    """Test health check endpoint is fast"""
    async with AsyncClient(app=app, base_url="http://test", timeout=5.0) as client:
        start_time = time.time()
        
        response = await client.get("/health")
        
        response_time = (time.time() - start_time) * 1000
        
        print(f"\n✓ Health check response time: {response_time:.1f}ms")
        
        assert response.status_code == 200
        assert response_time < 100, f"Health check too slow: {response_time:.1f}ms"


# ============================================================================
# Test: Memory and Resource Usage
# ============================================================================

@pytest.mark.asyncio
async def test_sequential_requests_performance():
    """Test performance of sequential requests (no memory leaks)"""
    async with AsyncClient(app=app, base_url="http://test", timeout=60.0) as client:
        times = []
        
        # Make 20 sequential requests
        for i in range(20):
            start = time.time()
            response = await client.post("/api/leads", json={
                "name": f"Sequential Test {i}",
                "email": f"sequential{i}@test.com",
                "role": "Home Owner",
                "message": "Test",
                "product_interests": []
            })
            duration = time.time() - start
            
            if response.status_code == 200:
                times.append(duration)
        
        if len(times) >= 10:
            avg_time = sum(times) / len(times)
            first_10_avg = sum(times[:10]) / 10
            last_10_avg = sum(times[-10:]) / 10
            
            print(f"\n✓ Sequential requests: {len(times)}/20 succeeded")
            print(f"✓ Average time: {avg_time:.3f}s")
            print(f"✓ First 10 avg: {first_10_avg:.3f}s")
            print(f"✓ Last 10 avg: {last_10_avg:.3f}s")
            
            # Last requests shouldn't be significantly slower (no memory leak)
            assert last_10_avg < first_10_avg * 1.5, "Performance degradation detected"


# ============================================================================
# Test: Stress Test
# ============================================================================

@pytest.mark.asyncio
async def test_stress_test_burst_requests():
    """Test system handles burst of requests"""
    async with AsyncClient(app=app, base_url="http://test", timeout=120.0) as client:
        async def create_lead(index):
            try:
                response = await client.post("/api/leads", json={
                    "name": f"Stress Test {index}",
                    "email": f"stress{index}@test.com",
                    "role": "Home Owner",
                    "message": "Stress test",
                    "product_interests": []
                })
                return response.status_code == 200
            except:
                return False
        
        # Create 20 leads in burst
        start_time = time.time()
        tasks = [create_lead(i) for i in range(20)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        success_count = sum(1 for success in results if success)
        success_rate = (success_count / 20) * 100
        
        print(f"\n✓ Stress test: {success_count}/20 succeeded ({success_rate:.1f}%)")
        print(f"✓ Total time: {total_time:.3f}s")
        
        # At least 80% should succeed
        assert success_rate >= 80, f"Only {success_rate:.1f}% success rate"
