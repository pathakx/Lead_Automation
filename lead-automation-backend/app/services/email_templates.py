from typing import Dict, List

class EmailTemplates:
    """Centralized email template management for all lead communication"""
    
    @staticmethod
    def acknowledgement(name: str, products: List[str]) -> Dict[str, str]:
        """
        Acknowledgement email for all new leads
        Sent immediately upon lead submission
        """
        subject = f"Thank you for your inquiry, {name}!"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .product-list {{ background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .product-list li {{ margin: 8px 0; }}
                .footer {{ background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 5px 5px; font-size: 12px; color: #6b7280; }}
                .cta-button {{ display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Thank you for contacting us!</h2>
                </div>
                <div class="content">
                    <p>Dear {name},</p>
                    <p>We've received your inquiry and appreciate your interest in our products. Our team is reviewing your request.</p>
                    
                    <h3 style="color: #2563eb;">Products You're Interested In:</h3>
                    <ul class="product-list">
                        {''.join([f"<li style='margin: 5px 0;'><strong>{product}</strong></li>" for product in products])}
                    </ul>
                    
                    <p><strong>What happens next?</strong></p>
                    <ul>
                        <li>Our team will review your requirements</li>
                        <li>We'll prepare a customized quote</li>
                        <li>You'll hear from us within 24 hours</li>
                    </ul>
                    
                    <p>If you have any urgent questions, feel free to reply to this email or call us at <strong>+91 1800-XXX-XXXX</strong></p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong>The Sales Team</strong></p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                    <p>&copy; 2024 Lead Automation System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html": html}
    
    @staticmethod
    def immediate_response_high_priority(name: str, products: List[str]) -> Dict[str, str]:
        """
        Immediate response for high-priority leads
        Sent to architects, builders, and urgent requests
        """
        subject = f"🚀 Priority Response: Your Quote Request - {name}"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .urgent-banner {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .highlight-box {{ background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; }}
                .product-list {{ background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .next-steps {{ background-color: #dbeafe; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 5px 5px; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="urgent-banner">
                    <h2 style="margin: 0;">⚡ Priority Request Received</h2>
                    <p style="margin: 10px 0 0 0;">Your inquiry has been marked as HIGH PRIORITY</p>
                </div>
                <div class="content">
                    <p>Dear {name},</p>
                    <p>Thank you for your urgent inquiry. We understand the importance of your project and have <strong>prioritized your request</strong> for immediate attention.</p>
                    
                    <div class="highlight-box">
                        <p style="margin: 0;"><strong>⏰ Response Time Commitment:</strong></p>
                        <p style="margin: 5px 0 0 0;">Our senior sales representative will contact you within the next <strong>1 hour</strong>.</p>
                    </div>
                    
                    <h3 style="color: #2563eb;">Products Requested:</h3>
                    <ul class="product-list">
                        {''.join([f"<li style='margin: 5px 0;'><strong>{product}</strong></li>" for product in products])}
                    </ul>
                    
                    <div class="next-steps">
                        <p style="margin: 0 0 10px 0;"><strong>📋 Next Steps:</strong></p>
                        <ol style="margin: 0; padding-left: 20px;">
                            <li>Our team is preparing your customized quote</li>
                            <li>A senior representative will call you shortly</li>
                            <li>We'll discuss your specific requirements</li>
                            <li>You'll receive a detailed proposal via email</li>
                        </ol>
                    </div>
                    
                    <p><strong>Need immediate assistance?</strong></p>
                    <p>Call our priority hotline: <strong style="color: #2563eb; font-size: 18px;">+91 1800-XXX-XXXX</strong></p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong>Priority Sales Team</strong></p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Lead Automation System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html": html}
    
    @staticmethod
    def nurture_day_0(name: str) -> Dict[str, str]:
        """
        Day 0 nurture email - Welcome sequence
        Sent 2 hours after initial acknowledgement
        """
        subject = f"Welcome! Here's what you need to know - {name}"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .benefits {{ background-color: #f0fdf4; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .resources {{ background-color: #f3f4f6; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 5px 5px; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Welcome to Our Community!</h2>
                </div>
                <div class="content">
                    <p>Hi {name},</p>
                    <p>Thank you for your interest in our products. We're excited to help you find the perfect solution for your project!</p>
                    
                    <div class="benefits">
                        <h3 style="color: #10b981; margin-top: 0;">Why Choose Us?</h3>
                        <ul style="margin: 10px 0;">
                            <li>✅ <strong>Premium Quality</strong> - Industry-leading materials</li>
                            <li>✅ <strong>Expert Support</strong> - 10+ years of experience</li>
                            <li>✅ <strong>Competitive Pricing</strong> - Best value for money</li>
                            <li>✅ <strong>Fast Delivery</strong> - On-time, every time</li>
                            <li>✅ <strong>Installation Help</strong> - Professional guidance</li>
                        </ul>
                    </div>
                    
                    <div class="resources">
                        <p style="margin: 0 0 10px 0;"><strong>📚 Helpful Resources:</strong></p>
                        <ul style="margin: 0;">
                            <li><a href="#" style="color: #2563eb;">Product Catalog</a> - Browse our complete range</li>
                            <li><a href="#" style="color: #2563eb;">Installation Guide</a> - Step-by-step instructions</li>
                            <li><a href="#" style="color: #2563eb;">Customer Testimonials</a> - See what others say</li>
                            <li><a href="#" style="color: #2563eb;">Design Gallery</a> - Get inspired</li>
                        </ul>
                    </div>
                    
                    <p><strong>Have questions?</strong> Our team is here to help!</p>
                    <p>Reply to this email or call us at <strong>+91 1800-XXX-XXXX</strong></p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong>The Sales Team</strong></p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Lead Automation System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html": html}
    
    @staticmethod
    def nurture_day_3(name: str) -> Dict[str, str]:
        """
        Day 3 nurture email - Special offer
        Sent 3 days after initial contact
        """
        subject = f"Still interested? Here's a special offer - {name}"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
                .offer-box {{ background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; border: 2px solid #f59e0b; }}
                .cta-button {{ display: inline-block; background-color: #2563eb; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                .footer {{ background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 5px 5px; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">We Haven't Forgotten About You!</h2>
                </div>
                <div class="content">
                    <p>Hi {name},</p>
                    <p>We noticed you were interested in our products a few days ago. We'd love to help you move forward with your project!</p>
                    
                    <div class="offer-box">
                        <h2 style="color: #92400e; margin: 0 0 15px 0;">🎁 Special Offer Just for You</h2>
                        <p style="font-size: 32px; font-weight: bold; color: #92400e; margin: 10px 0;">10% OFF</p>
                        <p style="font-size: 18px; margin: 10px 0;">on your first order</p>
                        <p style="font-size: 14px; color: #78350f; margin: 15px 0 0 0;">Use code: <strong style="font-size: 18px;">WELCOME10</strong></p>
                        <p style="font-size: 12px; color: #78350f; margin: 5px 0 0 0;">Valid for 7 days</p>
                    </div>
                    
                    <p><strong>Why wait?</strong> Here's what you get:</p>
                    <ul>
                        <li>💰 <strong>10% discount</strong> on your entire order</li>
                        <li>🚚 <strong>Free shipping</strong> on orders over ₹50,000</li>
                        <li>📞 <strong>Priority support</strong> from our experts</li>
                        <li>✅ <strong>Quality guarantee</strong> on all products</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="#" class="cta-button">Get Your Quote Now</a>
                    </div>
                    
                    <p>Have questions? Reply to this email or schedule a free consultation with our team!</p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong>The Sales Team</strong></p>
                </div>
                <div class="footer">
                    <p>Offer expires in 7 days. Terms and conditions apply.</p>
                    <p>&copy; 2024 Lead Automation System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html": html}
    
    @staticmethod
    def follow_up_reminder(name: str, action: str, scheduled_date: str) -> Dict[str, str]:
        """
        Follow-up reminder for sales team
        Internal email to remind team of pending actions
        """
        subject = f"⏰ Follow-up Reminder: {name} - {action}"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .reminder-banner {{ background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; margin-bottom: 20px; }}
                .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 5px; }}
                .info-box {{ background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .cta-button {{ display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="reminder-banner">
                    <h2 style="color: #92400e; margin: 0 0 10px 0;">📅 Follow-up Action Required</h2>
                    <p style="margin: 0;">This is an automated reminder for a pending follow-up task.</p>
                </div>
                <div class="content">
                    <div class="info-box">
                        <p style="margin: 5px 0;"><strong>Lead Name:</strong> {name}</p>
                        <p style="margin: 5px 0;"><strong>Action Required:</strong> {action}</p>
                        <p style="margin: 5px 0;"><strong>Scheduled For:</strong> {scheduled_date}</p>
                    </div>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ol>
                        <li>Review the lead details in the admin panel</li>
                        <li>Complete the required action ({action})</li>
                        <li>Update the lead status after completion</li>
                        <li>Log any notes or outcomes</li>
                    </ol>
                    
                    <p><strong>⚠️ Important:</strong> Please complete this follow-up action to maintain SLA compliance and ensure customer satisfaction.</p>
                    
                    <div style="text-align: center;">
                        <a href="#" class="cta-button">View Lead Details</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html": html}
