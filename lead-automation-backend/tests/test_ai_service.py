import pytest
from app.services.ai_service import AIService
from unittest.mock import Mock, patch, AsyncMock
import json

@pytest.fixture
def ai_service():
    """Create AI service instance for testing"""
    return AIService(api_key="test_api_key_12345")


# ============================================================================
# Test: High-Priority Lead Categorization
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_high_priority_architect(ai_service):
    """Test high-priority architect lead categorization"""
    lead_data = {
        "role": "Architect",
        "location": "Mumbai",
        "products": ["Premium Flooring", "Designer Wall Panels"],
        "message": "Need urgent quote for 5000 sq ft luxury project"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "high",
            "intent": "quote_request",
            "lead_type": "architect",
            "suggested_actions": ["call", "send_quote"],
            "reasoning": "Architect with urgent quote request for large luxury project"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        # Verify output
        assert result["output"]["priority"] == "high"
        assert result["output"]["intent"] == "quote_request"
        assert result["output"]["lead_type"] == "architect"
        assert "call" in result["output"]["suggested_actions"]
        
        # Verify metadata
        assert result["method"] == "ai"
        assert "model" in result
        assert "prompt_version" in result
        assert "timestamp" in result
        assert result["attempt"] == 1


@pytest.mark.asyncio
async def test_categorize_lead_high_priority_builder(ai_service):
    """Test high-priority builder lead categorization"""
    lead_data = {
        "role": "Builder",
        "location": "Pune",
        "products": ["Bulk Flooring"],
        "message": "Bulk pricing needed for 50 unit residential complex"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "high",
            "intent": "quote_request",
            "lead_type": "builder",
            "suggested_actions": ["call", "send_quote"],
            "reasoning": "Builder requesting bulk pricing for large project"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        assert result["output"]["priority"] == "high"
        assert result["output"]["lead_type"] == "builder"
        assert result["method"] == "ai"


# ============================================================================
# Test: Medium-Priority Lead Categorization
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_medium_priority_homeowner(ai_service):
    """Test medium-priority home owner lead categorization"""
    lead_data = {
        "role": "Home Owner",
        "location": "Delhi",
        "products": ["Laminate Flooring"],
        "message": "Need quote for home renovation, 1500 sq ft"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "medium",
            "intent": "quote_request",
            "lead_type": "homeowner",
            "suggested_actions": ["email", "send_quote"],
            "reasoning": "Home owner requesting quote for renovation"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        assert result["output"]["priority"] == "medium"
        assert result["output"]["lead_type"] == "homeowner"


@pytest.mark.asyncio
async def test_categorize_lead_medium_priority_contractor(ai_service):
    """Test medium-priority contractor lead categorization"""
    lead_data = {
        "role": "Contractor",
        "location": "Bangalore",
        "products": ["Wall Panels"],
        "message": "Looking for pricing for upcoming project"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "medium",
            "intent": "quote_request",
            "lead_type": "contractor",
            "suggested_actions": ["email", "send_quote"],
            "reasoning": "Contractor with specific inquiry"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        assert result["output"]["priority"] == "medium"
        assert result["output"]["lead_type"] == "contractor"


# ============================================================================
# Test: Low-Priority Lead Categorization
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_low_priority_browsing(ai_service):
    """Test low-priority browsing lead categorization"""
    lead_data = {
        "role": "Home Owner",
        "location": "Chennai",
        "products": ["Basic Flooring"],
        "message": "Just browsing different flooring options"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "low",
            "intent": "information",
            "lead_type": "homeowner",
            "suggested_actions": ["nurture", "email"],
            "reasoning": "Home owner browsing without immediate purchase intent"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        assert result["output"]["priority"] == "low"
        assert result["output"]["intent"] == "information"


# ============================================================================
# Test: Fallback Categorization
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_fallback_on_api_failure(ai_service):
    """Test fallback categorization when AI API fails"""
    lead_data = {
        "role": "Home Owner",
        "location": "Delhi",
        "products": ["Flooring"],
        "message": "Just looking at options"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.side_effect = Exception("API Error")
        
        result = await ai_service.categorize_lead(lead_data, retry_count=1)
        
        # Should use fallback
        assert result["method"] == "fallback"
        assert result["model"] == "rule_based_fallback"
        assert "output" in result
        assert "priority" in result["output"]


def test_fallback_categorization_urgent_keywords(ai_service):
    """Test fallback detects urgent keywords"""
    lead_input = {
        "role": "Contractor",
        "location": "Mumbai",
        "products": ["Flooring"],
        "message": "URGENT: Need quote ASAP for project starting tomorrow"
    }
    
    result = ai_service.fallback_categorization(lead_input)
    
    assert result["output"]["priority"] == "high"
    assert result["output"]["intent"] == "quote_request"
    assert result["method"] == "fallback"


def test_fallback_categorization_quote_keywords(ai_service):
    """Test fallback detects quote keywords"""
    lead_input = {
        "role": "Home Owner",
        "location": "Pune",
        "products": ["Wall Panels"],
        "message": "Can you provide a price estimate for wall panels?"
    }
    
    result = ai_service.fallback_categorization(lead_input)
    
    assert result["output"]["intent"] == "quote_request"
    assert result["output"]["priority"] in ["high", "medium"]


def test_fallback_categorization_low_priority(ai_service):
    """Test fallback for browsing leads without urgent keywords"""
    lead_input = {
        "role": "Home Owner",
        "location": "Chennai",
        "products": [],
        "message": "Just exploring different options"
    }
    
    result = ai_service.fallback_categorization(lead_input)
    
    assert result["output"]["priority"] == "medium"  # Default when no urgent keywords
    assert result["method"] == "fallback"


def test_fallback_categorization_role_mapping(ai_service):
    """Test fallback correctly maps roles to lead types"""
    test_cases = [
        ("Architect", "architect"),
        ("Builder", "builder"),
        ("Contractor", "contractor"),
        ("Home Owner", "home_owner"),
    ]
    
    for role, expected_type in test_cases:
        lead_input = {
            "role": role,
            "location": "Test",
            "products": [],
            "message": "Test message"
        }
        
        result = ai_service.fallback_categorization(lead_input)
        assert result["output"]["lead_type"] == expected_type


# ============================================================================
# Test: Retry Logic
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_retry_logic_success_on_second_attempt(ai_service):
    """Test retry logic succeeds on second attempt"""
    lead_data = {
        "role": "Builder",
        "location": "Mumbai",
        "products": ["Bulk Flooring"],
        "message": "Bulk order needed"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        # Fail once, succeed on second attempt
        mock_api.side_effect = [
            Exception("Timeout"),
            {
                "priority": "high",
                "intent": "quote_request",
                "lead_type": "builder",
                "suggested_actions": ["call", "send_quote"],
                "reasoning": "Builder bulk order"
            }
        ]
        
        result = await ai_service.categorize_lead(lead_data, retry_count=3)
        
        assert result["method"] == "ai"
        assert result["attempt"] == 2
        assert result["output"]["priority"] == "high"


@pytest.mark.asyncio
async def test_categorize_lead_retry_logic_success_on_third_attempt(ai_service):
    """Test retry logic succeeds on third attempt"""
    lead_data = {
        "role": "Architect",
        "location": "Delhi",
        "products": ["Premium Flooring"],
        "message": "Urgent quote"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        # Fail twice, succeed on third attempt
        mock_api.side_effect = [
            Exception("Timeout"),
            Exception("Rate limit"),
            {
                "priority": "high",
                "intent": "quote_request",
                "lead_type": "architect",
                "suggested_actions": ["call", "send_quote"],
                "reasoning": "Architect urgent quote"
            }
        ]
        
        result = await ai_service.categorize_lead(lead_data, retry_count=3)
        
        assert result["method"] == "ai"
        assert result["attempt"] == 3


@pytest.mark.asyncio
async def test_categorize_lead_retry_exhausted_uses_fallback(ai_service):
    """Test fallback is used when all retries are exhausted"""
    lead_data = {
        "role": "Home Owner",
        "location": "Bangalore",
        "products": ["Flooring"],
        "message": "Need quote"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        # Fail all attempts
        mock_api.side_effect = [
            Exception("Error 1"),
            Exception("Error 2"),
            Exception("Error 3")
        ]
        
        result = await ai_service.categorize_lead(lead_data, retry_count=3)
        
        # Should use fallback after all retries
        assert result["method"] == "fallback"
        assert result["model"] == "rule_based_fallback"


# ============================================================================
# Test: Input Validation
# ============================================================================

def test_fallback_categorization_handles_missing_fields(ai_service):
    """Test fallback handles missing or None fields gracefully"""
    lead_input = {
        "role": None,
        "location": None,
        "products": None,
        "message": None
    }
    
    result = ai_service.fallback_categorization(lead_input)
    
    # Should not crash and return valid result
    assert "output" in result
    assert "priority" in result["output"]
    assert "lead_type" in result["output"]


def test_fallback_categorization_handles_empty_message(ai_service):
    """Test fallback handles empty message"""
    lead_input = {
        "role": "Home Owner",
        "location": "Mumbai",
        "products": [],
        "message": ""
    }
    
    result = ai_service.fallback_categorization(lead_input)
    
    assert result["output"]["priority"] == "medium"  # Default
    assert result["output"]["intent"] == "product_info"  # Default


# ============================================================================
# Test: Model and Prompt Versioning
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_includes_version_info(ai_service):
    """Test that categorization includes model and prompt version"""
    lead_data = {
        "role": "Architect",
        "location": "Mumbai",
        "products": ["Flooring"],
        "message": "Test"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "high",
            "intent": "quote_request",
            "lead_type": "architect",
            "suggested_actions": ["call"],
            "reasoning": "Test"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        # Verify version tracking
        assert "model" in result
        assert "prompt_version" in result
        assert result["model"] == ai_service.MODEL_VERSION
        assert result["prompt_version"] == ai_service.PROMPT_VERSION


# ============================================================================
# Test: Input Storage for Replay
# ============================================================================

@pytest.mark.asyncio
async def test_categorize_lead_stores_input_for_replay(ai_service):
    """Test that original input is stored for replay capability"""
    lead_data = {
        "role": "Builder",
        "location": "Pune",
        "products": ["Product 1", "Product 2"],
        "message": "Test message"
    }
    
    with patch.object(ai_service, '_call_groq_api') as mock_api:
        mock_api.return_value = {
            "priority": "high",
            "intent": "quote_request",
            "lead_type": "builder",
            "suggested_actions": ["call"],
            "reasoning": "Test"
        }
        
        result = await ai_service.categorize_lead(lead_data)
        
        # Verify input is stored
        assert "input" in result
        assert result["input"]["role"] == "Builder"
        assert result["input"]["location"] == "Pune"
        assert result["input"]["products"] == ["Product 1", "Product 2"]
        assert result["input"]["message"] == "Test message"
