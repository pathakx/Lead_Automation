from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
from app.utils.db import (
    insert_record,
    update_record,
    get_record,
    query_records
)
from app.services.ai_service import get_ai_service
from app.services.email_service import get_email_service

logger = logging.getLogger(__name__)

class LeadService:
    """Business logic for lead processing"""
    
    def __init__(self):
        self.ai_service = get_ai_service()
        self.email_service = get_email_service()
    
    async def create_lead_with_products(
        self,
        lead_data: Dict[str, Any],
        product_interests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Complete lead capture workflow:
        1. Insert lead
        2. Insert products
        3. AI categorization
        4. Log AI activity
        5. Auto-assign
        6. Send acknowledgement email
        7. Create follow-up
        """
        
        # Step 1: Insert lead
        lead = await insert_record("leads", {
            "name": lead_data["name"],
            "email": lead_data["email"],
            "phone": lead_data.get("phone"),
            "company": lead_data.get("company"),
            "role": lead_data.get("role"),
            "location": lead_data.get("location"),
            "message": lead_data.get("message"),
            "source": lead_data.get("source", "website_form"),
            "status": "new"
        })
        
        lead_id = lead["id"]
        logger.info(f"Created lead {lead_id}")
        
        # Step 2: Insert products
        products = []
        for product in product_interests:
            p = await insert_record("lead_products", {
                "lead_id": lead_id,
                "category": product["category"],
                "product": product["product"],
                "quantity": product.get("quantity"),
                "notes": product.get("notes")
            })
            products.append(p)
        
        # Step 3: AI Categorization
        ai_result = await self.ai_service.categorize_lead({
            "role": lead_data.get("role"),
            "location": lead_data.get("location"),
            "products": [p["product"] for p in product_interests],
            "message": lead_data.get("message")
        })
        
        # Step 4: Log AI activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "ai_result",
            "status": "completed",
            "message": "AI analyzed lead and suggested priority action",
            "actor_type": "ai",
            "metadata": ai_result
        })
        
        # Step 5: Auto-assign based on priority
        priority = ai_result["output"]["priority"]
        sla_hours = 1 if priority == "high" else 24
        
        assignment = await insert_record("assignments", {
            "lead_id": lead_id,
            "owner_id": "system_auto",  # TODO: Implement round-robin assignment
            "owner_name": "Auto-assigned",
            "sla_deadline": (datetime.utcnow() + timedelta(hours=sla_hours)).isoformat()
        })
        
        # Log assignment activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "assignment",
            "status": "completed",
            "message": f"Lead auto-assigned with {sla_hours}h SLA",
            "actor_type": "system",
            "metadata": {
                "owner_id": assignment["owner_id"],
                "owner_name": assignment["owner_name"],
                "sla_deadline": assignment["sla_deadline"]
            }
        })
        
        # Step 6: Send acknowledgement email
        email_result = await self.email_service.send_acknowledgement(
            to_email=lead_data["email"],
            name=lead_data["name"],
            products=[p["product"] for p in product_interests]
        )
        
        # Log email activity
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "email",
            "status": "completed" if email_result["success"] else "failed",
            "message": "Acknowledgement email sent" if email_result["success"] else "Email failed",
            "actor_type": "system",
            "metadata": email_result
        })
        
        # Update first_response_at
        if email_result["success"]:
            await update_record("leads", lead_id, {
                "first_response_at": datetime.utcnow().isoformat()
            })
        
        # Step 6.5: Check if approval needed for high-value scenarios
        approval_needed = False
        approval_reason = ""
        approval_details = {}
        
        # Calculate total quantity from products (handle string values)
        total_quantity = 0
        for p in product_interests:
            qty = p.get("quantity", 0)
            if qty:
                try:
                    total_quantity += int(qty) if isinstance(qty, str) else qty
                except (ValueError, TypeError):
                    pass  # Skip invalid quantities
        
        # Scenario 1: Large Quantity Orders (>= 100 units)
        if total_quantity >= 100:
            approval_needed = True
            approval_reason = "large_quantity_order"
            approval_details = {
                "total_quantity": total_quantity,
                "products": [p["product"] for p in product_interests],
                "threshold": 100,
                "message": f"Large order of {total_quantity} units requires manager approval"
            }
        
        # Scenario 2: High-Priority Professional Buyers (Architects/Builders)
        elif priority == "high" and lead_data.get("role") in ["Architect", "Builder"]:
            approval_needed = True
            approval_reason = "high_priority_professional"
            approval_details = {
                "role": lead_data.get("role"),
                "priority": priority,
                "products": [p["product"] for p in product_interests],
                "message": f"High-priority {lead_data.get('role')} quote requires approval"
            }
        
        # Scenario 3: Bulk Keywords in Message
        bulk_keywords = ["bulk", "wholesale", "project", "commercial", "discount"]
        message_lower = (lead_data.get("message") or "").lower()
        if any(keyword in message_lower for keyword in bulk_keywords):
            approval_needed = True
            approval_reason = "bulk_discount_request"
            approval_details = {
                "message_snippet": lead_data.get("message")[:200],
                "keywords_found": [kw for kw in bulk_keywords if kw in message_lower],
                "products": [p["product"] for p in product_interests],
                "message": "Bulk/discount request requires pricing approval"
            }
        
        # Create approval if needed
        if approval_needed:
            logger.info(f"Creating approval for lead {lead_id}: {approval_reason}")
            
            await insert_record("lead_activity", {
                "lead_id": lead_id,
                "type": "approval",
                "status": "pending",
                "message": f"Approval Required: {approval_details['message']}",
                "actor_type": "system",
                "metadata": {
                    "approval_type": approval_reason,
                    "lead_name": lead_data["name"],
                    "lead_email": lead_data["email"],
                    "lead_phone": lead_data.get("phone"),
                    "lead_role": lead_data.get("role"),
                    "lead_company": lead_data.get("company"),
                    "priority": priority,
                    "details": approval_details,
                    "created_at": datetime.utcnow().isoformat()
                }
            })
        
        
        # Step 7: Create follow-up based on priority
        # All leads get a follow-up, but timing varies by priority
        follow_up_schedule = {
            "high": {
                "minutes": 30,
                "action": "call",
                "message": "High-priority lead - urgent call required",
                "reason": "high_priority_lead"
            },
            "medium": {
                "hours": 24,
                "action": "email",
                "message": "Medium-priority lead - follow up within 24 hours",
                "reason": "medium_priority_lead"
            },
            "low": {
                "days": 3,
                "action": "nurture",
                "message": "Low-priority lead - add to nurture sequence",
                "reason": "low_priority_lead"
            }
        }
        
        schedule_config = follow_up_schedule.get(priority, follow_up_schedule["medium"])
        
        # Calculate scheduled time based on priority
        if "minutes" in schedule_config:
            scheduled_time = datetime.utcnow() + timedelta(minutes=schedule_config["minutes"])
        elif "hours" in schedule_config:
            scheduled_time = datetime.utcnow() + timedelta(hours=schedule_config["hours"])
        else:  # days
            scheduled_time = datetime.utcnow() + timedelta(days=schedule_config["days"])
        
        await insert_record("lead_activity", {
            "lead_id": lead_id,
            "type": "follow_up",
            "status": "pending",
            "message": schedule_config["message"],
            "metadata": {
                "action": schedule_config["action"],
                "scheduled_for": scheduled_time.isoformat(),
                "reason": schedule_config["reason"],
                "priority": priority
            }
        })
        
        
        return {
            "lead": lead,
            "products": products,
            "ai_categorization": ai_result["output"],
            "assignment": assignment,
            "email_sent": email_result["success"]
        }


# Initialize service
lead_service = None

def get_lead_service() -> LeadService:
    """Get or create lead service instance"""
    global lead_service
    if lead_service is None:
        lead_service = LeadService()
    return lead_service
