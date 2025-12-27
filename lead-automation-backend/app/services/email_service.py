import resend
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Email service using Resend API"""
    
    def __init__(self, api_key: str, from_email: str):
        resend.api_key = api_key
        self.from_email = from_email
    
    async def send_acknowledgement(
        self,
        to_email: str,
        name: str,
        products: List[str]
    ) -> Dict[str, Any]:
        """Send acknowledgement email to new lead"""
        
        subject = f"Thank you for your inquiry, {name}!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Thank you for contacting us!</h2>
            <p>Dear {name},</p>
            <p>We've received your inquiry about:</p>
            <ul style="background-color: #f3f4f6; padding: 15px; border-radius: 5px;">
                {"".join([f"<li style='margin: 5px 0;'>{product}</li>" for product in products])}
            </ul>
            <p>Our team will review your request and get back to you within 24 hours.</p>
            <p style="margin-top: 30px;">Best regards,<br><strong>The Sales Team</strong></p>
            <hr style="margin-top: 30px; border: none; border-top: 1px solid #e5e7eb;">
            <p style="font-size: 12px; color: #6b7280;">This is an automated message. Please do not reply to this email.</p>
        </body>
        </html>
        """
        
        try:
            result = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })
            
            logger.info(f"Acknowledgement email sent to {to_email}, ID: {result['id']}")
            
            return {
                "success": True,
                "resend_id": result['id'],
                "template": "acknowledgement",
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send acknowledgement email to {to_email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "template": "acknowledgement"
            }
    
    async def send_template_email(
        self,
        to_email: str,
        template_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send email using centralized template system
        
        Args:
            to_email: Recipient email address
            template_name: Name of the template method in EmailTemplates class
            **kwargs: Template-specific parameters
        
        Returns:
            Dict with success status, resend_id, and metadata
        """
        from .email_templates import EmailTemplates
        
        # Get template method
        template_func = getattr(EmailTemplates, template_name, None)
        if not template_func:
            logger.error(f"Template '{template_name}' not found")
            return {
                "success": False,
                "error": f"Template '{template_name}' not found",
                "template": template_name
            }
        
        try:
            # Generate email content from template
            template = template_func(**kwargs)
            
            # Send email
            result = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": template["subject"],
                "html": template["html"]
            })
            
            logger.info(f"Template email '{template_name}' sent to {to_email}, ID: {result['id']}")
            
            return {
                "success": True,
                "resend_id": result['id'],
                "template": template_name,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send template email '{template_name}' to {to_email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "template": template_name
            }
    
    async def send_custom_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> Dict[str, Any]:
        """Send custom email"""
        
        try:
            result = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })
            
            logger.info(f"Custom email sent to {to_email}, ID: {result['id']}")
            
            return {
                "success": True,
                "resend_id": result['id'],
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Initialize email service (singleton)
email_service = None

def get_email_service() -> EmailService:
    """Get or create email service instance"""
    global email_service
    if email_service is None:
        from app.config import settings
        email_service = EmailService(
            api_key=settings.RESEND_API_KEY,
            from_email=settings.RESEND_FROM_EMAIL
        )
    return email_service
