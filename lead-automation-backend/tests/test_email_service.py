import pytest
from app.services.email_service import EmailService
from app.services.email_templates import EmailTemplates
from unittest.mock import Mock, patch, AsyncMock
import resend

@pytest.fixture
def email_service():
    """Create email service instance for testing"""
    return EmailService(api_key="test_resend_key_12345", from_email="test@example.com")


# ============================================================================
# Test: Acknowledgement Email
# ============================================================================

@pytest.mark.asyncio
async def test_send_acknowledgement_email_success(email_service):
    """Test sending acknowledgement email successfully"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'test_email_id_123'}
        
        result = await email_service.send_acknowledgement(
            to_email="customer@example.com",
            name="Vikas Pathak",
            products=["Premium Flooring", "Designer Wall Panels"]
        )
        
        # Verify success
        assert result["success"] is True
        assert result["resend_id"] == "test_email_id_123"
        assert result["template"] == "acknowledgement"
        assert "sent_at" in result
        
        # Verify email was sent
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        assert call_args["from"] == "test@example.com"
        assert call_args["to"] == "customer@example.com"
        assert "Vikas Pathak" in call_args["subject"]


@pytest.mark.asyncio
async def test_send_acknowledgement_email_with_multiple_products(email_service):
    """Test acknowledgement email with multiple products"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'email_123'}
        
        products = ["Product 1", "Product 2", "Product 3", "Product 4"]
        
        result = await email_service.send_acknowledgement(
            to_email="test@test.com",
            name="Test User",
            products=products
        )
        
        assert result["success"] is True
        
        # Verify all products are in email
        call_args = mock_send.call_args[0][0]
        html_content = call_args["html"]
        for product in products:
            assert product in html_content


@pytest.mark.asyncio
async def test_send_acknowledgement_email_api_failure(email_service):
    """Test acknowledgement email handles API failures gracefully"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.side_effect = Exception("Resend API Error")
        
        result = await email_service.send_acknowledgement(
            to_email="test@example.com",
            name="Test User",
            products=["Product"]
        )
        
        # Should return failure
        assert result["success"] is False
        assert "error" in result
        assert result["template"] == "acknowledgement"


# ============================================================================
# Test: Template-Based Email Sending
# ============================================================================

@pytest.mark.asyncio
async def test_send_template_email_success(email_service):
    """Test template-based email sending"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'template_email_id'}
        
        result = await email_service.send_template_email(
            to_email="test@example.com",
            template_name="nurture_day_0",
            name="Jane Doe"
        )
        
        assert result["success"] is True
        assert result["template"] == "nurture_day_0"
        assert result["resend_id"] == "template_email_id"


@pytest.mark.asyncio
async def test_send_template_email_high_priority(email_service):
    """Test sending high-priority template email"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'priority_email_id'}
        
        result = await email_service.send_template_email(
            to_email="vip@example.com",
            template_name="immediate_response_high_priority",
            name="VIP Customer",
            products=["Premium Product"]
        )
        
        assert result["success"] is True
        assert result["template"] == "immediate_response_high_priority"
        
        # Verify email content
        call_args = mock_send.call_args[0][0]
        assert "Priority" in call_args["subject"] or "🚀" in call_args["subject"]


@pytest.mark.asyncio
async def test_send_template_email_nurture_day_3(email_service):
    """Test sending nurture day 3 email with special offer"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'nurture_email_id'}
        
        result = await email_service.send_template_email(
            to_email="customer@example.com",
            template_name="nurture_day_3",
            name="Customer Name"
        )
        
        assert result["success"] is True
        
        # Verify discount code is in email
        call_args = mock_send.call_args[0][0]
        html_content = call_args["html"]
        assert "WELCOME10" in html_content or "10%" in html_content


@pytest.mark.asyncio
async def test_send_template_email_invalid_template(email_service):
    """Test error handling for invalid template name"""
    result = await email_service.send_template_email(
        to_email="test@example.com",
        template_name="nonexistent_template",
        name="Test User"
    )
    
    assert result["success"] is False
    assert "not found" in result["error"]
    assert result["template"] == "nonexistent_template"


@pytest.mark.asyncio
async def test_send_template_email_missing_parameters(email_service):
    """Test template email with missing required parameters"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.side_effect = Exception("Missing parameter")
        
        result = await email_service.send_template_email(
            to_email="test@example.com",
            template_name="acknowledgement"
            # Missing 'name' parameter
        )
        
        assert result["success"] is False


# ============================================================================
# Test: Custom Email Sending
# ============================================================================

@pytest.mark.asyncio
async def test_send_custom_email_success(email_service):
    """Test sending custom email"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'custom_email_id'}
        
        result = await email_service.send_custom_email(
            to_email="custom@example.com",
            subject="Custom Subject",
            html_content="<html><body>Custom content</body></html>"
        )
        
        assert result["success"] is True
        assert result["resend_id"] == "custom_email_id"
        assert "sent_at" in result


@pytest.mark.asyncio
async def test_send_custom_email_failure(email_service):
    """Test custom email handles failures"""
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.side_effect = Exception("Send failed")
        
        result = await email_service.send_custom_email(
            to_email="test@example.com",
            subject="Test",
            html_content="<html>Test</html>"
        )
        
        assert result["success"] is False
        assert "error" in result


# ============================================================================
# Test: Email Templates
# ============================================================================

def test_email_template_acknowledgement():
    """Test acknowledgement template generation"""
    template = EmailTemplates.acknowledgement(
        name="Test User",
        products=["Product 1", "Product 2"]
    )
    
    assert "subject" in template
    assert "html" in template
    assert "Test User" in template["html"]
    assert "Product 1" in template["html"]
    assert "Product 2" in template["html"]
    assert "Thank you" in template["subject"]


def test_email_template_acknowledgement_single_product():
    """Test acknowledgement template with single product"""
    template = EmailTemplates.acknowledgement(
        name="Vikas Pathak",
        products=["Single Product"]
    )
    
    assert "Single Product" in template["html"]
    assert "Vikas Pathak" in template["html"]


def test_email_template_high_priority():
    """Test high-priority template generation"""
    template = EmailTemplates.immediate_response_high_priority(
        name="VIP Customer",
        products=["Premium Product"]
    )
    
    assert "subject" in template
    assert "html" in template
    assert "Priority" in template["subject"] or "🚀" in template["subject"]
    assert "VIP Customer" in template["html"]
    assert "Premium Product" in template["html"]
    
    # Should mention response time commitment
    assert "hour" in template["html"].lower() or "1 hour" in template["html"]


def test_email_template_nurture_day_0():
    """Test nurture day 0 template generation"""
    template = EmailTemplates.nurture_day_0(name="New Customer")
    
    assert "subject" in template
    assert "html" in template
    assert "New Customer" in template["html"]
    assert "Welcome" in template["subject"] or "welcome" in template["html"].lower()
    
    # Should have benefits or resources
    assert "benefit" in template["html"].lower() or "resource" in template["html"].lower()


def test_email_template_nurture_day_3():
    """Test nurture day 3 template generation"""
    template = EmailTemplates.nurture_day_3(name="Potential Customer")
    
    assert "subject" in template
    assert "html" in template
    assert "Potential Customer" in template["html"]
    
    # Should have discount code
    assert "WELCOME10" in template["html"]
    assert "10%" in template["html"] or "10" in template["html"]


def test_email_template_follow_up_reminder():
    """Test follow-up reminder template generation"""
    template = EmailTemplates.follow_up_reminder(
        name="Vikas Pathak",
        action="Call customer",
        scheduled_date="2024-12-27 15:00"
    )
    
    assert "subject" in template
    assert "html" in template
    assert "Vikas Pathak" in template["html"]
    assert "Call customer" in template["html"]
    assert "2024-12-27 15:00" in template["html"]
    assert "Reminder" in template["subject"] or "⏰" in template["subject"]


# ============================================================================
# Test: Email Content Validation
# ============================================================================

def test_email_template_html_structure():
    """Test that templates generate valid HTML structure"""
    template = EmailTemplates.acknowledgement(
        name="Test",
        products=["Product"]
    )
    
    html = template["html"]
    
    # Basic HTML structure
    assert "<html>" in html
    assert "</html>" in html
    assert "<body>" in html or "<div" in html
    
    # Should have styling
    assert "style" in html.lower()


def test_email_template_no_broken_placeholders():
    """Test that templates don't have broken placeholders"""
    templates_to_test = [
        EmailTemplates.acknowledgement(name="Test", products=["P1"]),
        EmailTemplates.immediate_response_high_priority(name="Test", products=["P1"]),
        EmailTemplates.nurture_day_0(name="Test"),
        EmailTemplates.nurture_day_3(name="Test"),
        EmailTemplates.follow_up_reminder(name="Test", action="Action", scheduled_date="Date")
    ]
    
    for template in templates_to_test:
        html = template["html"]
        subject = template["subject"]
        
        # Should not have unresolved placeholders
        assert "{" not in html or "{{" not in html
        assert "}" not in html or "}}" not in html
        assert "{" not in subject


def test_email_template_special_characters():
    """Test templates handle special characters correctly"""
    template = EmailTemplates.acknowledgement(
        name="Test & User <test@example.com>",
        products=["Product with 'quotes' and \"double quotes\""]
    )
    
    # Should not crash
    assert "subject" in template
    assert "html" in template


# ============================================================================
# Test: Email Service Configuration
# ============================================================================

def test_email_service_initialization():
    """Test email service initializes correctly"""
    service = EmailService(
        api_key="test_key",
        from_email="sender@example.com"
    )
    
    assert service.from_email == "sender@example.com"
    assert resend.api_key == "test_key"


def test_email_service_from_email_used():
    """Test that configured from_email is used in emails"""
    service = EmailService(
        api_key="test_key",
        from_email="custom@example.com"
    )
    
    with patch.object(resend.Emails, 'send') as mock_send:
        mock_send.return_value = {'id': 'test_id'}
        
        # Use asyncio.run for async test in sync function
        import asyncio
        asyncio.run(service.send_acknowledgement(
            to_email="recipient@example.com",
            name="Test",
            products=["Product"]
        ))
        
        call_args = mock_send.call_args[0][0]
        assert call_args["from"] == "custom@example.com"
