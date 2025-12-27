from typing import Dict, List, Any

"""
Automation Rules Configuration

This module defines workflow automation rules that trigger based on AI categorization.
Each rule specifies criteria for matching and actions to execute.

Actions are processed sequentially by the lead service.
"""

AUTOMATION_RULES = {
    "hot_lead": {
        "description": "High-priority leads requiring immediate attention",
        "criteria": {
            "priority": "high",
            "intent": "quote_request"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "immediate_response_high_priority",
                "delay_minutes": 0,
                "description": "Send priority response email immediately"
            },
            {
                "type": "create_follow_up",
                "action": "call",
                "due_in_hours": 1,
                "message": "Call high-priority lead immediately - urgent quote request",
                "description": "Schedule call within 1 hour"
            },
            {
                "type": "create_assignment",
                "sla_hours": 1,
                "owner": "senior_sales",
                "description": "Assign to senior sales with 1-hour SLA"
            },
            {
                "type": "create_approval",
                "approval_type": "high_value_lead",
                "requires_manager": True,
                "description": "Create approval for manager review"
            }
        ]
    },
    
    "warm_lead": {
        "description": "Medium-priority leads with specific interest",
        "criteria": {
            "priority": "medium"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "acknowledgement",
                "delay_minutes": 0,
                "description": "Send acknowledgement email immediately"
            },
            {
                "type": "send_email",
                "template": "nurture_day_0",
                "delay_hours": 2,
                "description": "Send welcome nurture email after 2 hours"
            },
            {
                "type": "create_follow_up",
                "action": "email",
                "due_in_days": 3,
                "message": "Send nurture day 3 email with special offer",
                "description": "Schedule nurture email for day 3"
            },
            {
                "type": "create_assignment",
                "sla_hours": 24,
                "owner": "sales_team",
                "description": "Assign to sales team with 24-hour SLA"
            }
        ]
    },
    
    "cold_lead": {
        "description": "Low-priority leads browsing or gathering information",
        "criteria": {
            "priority": "low",
            "intent": "information"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "nurture_day_0",
                "delay_minutes": 0,
                "description": "Send welcome email with resources"
            },
            {
                "type": "create_follow_up",
                "action": "email",
                "due_in_days": 7,
                "message": "Send nurture day 7 email - check if still interested",
                "description": "Schedule long-term nurture email"
            },
            {
                "type": "create_assignment",
                "sla_hours": 72,
                "owner": "marketing_team",
                "description": "Assign to marketing team with 72-hour SLA"
            }
        ]
    },
    
    "architect_vip": {
        "description": "VIP treatment for architects (high-value professional buyers)",
        "criteria": {
            "lead_type": "architect",
            "priority": "high"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "immediate_response_high_priority",
                "delay_minutes": 0,
                "description": "Send VIP priority response"
            },
            {
                "type": "create_follow_up",
                "action": "call",
                "due_in_minutes": 30,
                "message": "URGENT: Priority call to architect - VIP lead",
                "description": "Schedule immediate call within 30 minutes"
            },
            {
                "type": "create_approval",
                "approval_type": "architect_vip",
                "requires_manager": True,
                "description": "Create VIP approval for manager"
            },
            {
                "type": "create_assignment",
                "sla_hours": 1,
                "owner": "senior_sales",
                "description": "Assign to senior sales immediately"
            },
            {
                "type": "notify_sales",
                "channel": "slack",
                "message": "🚨 VIP Architect Lead Received - Immediate Action Required",
                "description": "Send Slack notification to sales team"
            }
        ]
    },
    
    "builder_bulk": {
        "description": "Builders with bulk orders or large projects",
        "criteria": {
            "lead_type": "builder",
            "priority": "high"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "immediate_response_high_priority",
                "delay_minutes": 0,
                "description": "Send priority response for bulk order"
            },
            {
                "type": "create_follow_up",
                "action": "call",
                "due_in_hours": 2,
                "message": "Call builder for bulk pricing discussion",
                "description": "Schedule call within 2 hours"
            },
            {
                "type": "create_assignment",
                "sla_hours": 2,
                "owner": "senior_sales",
                "description": "Assign to senior sales for bulk pricing"
            },
            {
                "type": "create_approval",
                "approval_type": "bulk_order",
                "requires_manager": True,
                "description": "Create approval for bulk pricing"
            }
        ]
    },
    
    "partnership_inquiry": {
        "description": "Partnership or dealer inquiries",
        "criteria": {
            "intent": "partnership"
        },
        "actions": [
            {
                "type": "send_email",
                "template": "acknowledgement",
                "delay_minutes": 0,
                "description": "Send acknowledgement for partnership inquiry"
            },
            {
                "type": "create_follow_up",
                "action": "call",
                "due_in_hours": 24,
                "message": "Call regarding partnership/dealer inquiry",
                "description": "Schedule partnership discussion call"
            },
            {
                "type": "create_assignment",
                "sla_hours": 48,
                "owner": "business_development",
                "description": "Assign to business development team"
            },
            {
                "type": "create_approval",
                "approval_type": "partnership",
                "requires_manager": True,
                "description": "Create approval for partnership review"
            }
        ]
    }
}


def get_matching_rule(ai_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find the best matching automation rule based on AI categorization
    
    Args:
        ai_result: AI categorization output containing priority, intent, lead_type
    
    Returns:
        Dict containing rule name and actions to execute
    
    Priority order:
    1. Specific combinations (architect + high, builder + high)
    2. Intent-based (partnership)
    3. Priority-based (high, medium, low)
    """
    
    priority = ai_result.get("priority", "medium")
    intent = ai_result.get("intent", "information")
    lead_type = ai_result.get("lead_type", "homeowner")
    
    # Check for specific high-value combinations first
    if lead_type == "architect" and priority == "high":
        return {
            "rule_name": "architect_vip",
            **AUTOMATION_RULES["architect_vip"]
        }
    
    if lead_type == "builder" and priority == "high":
        return {
            "rule_name": "builder_bulk",
            **AUTOMATION_RULES["builder_bulk"]
        }
    
    # Check for partnership inquiries
    if intent == "partnership":
        return {
            "rule_name": "partnership_inquiry",
            **AUTOMATION_RULES["partnership_inquiry"]
        }
    
    # Check priority-based rules
    if priority == "high" and intent == "quote_request":
        return {
            "rule_name": "hot_lead",
            **AUTOMATION_RULES["hot_lead"]
        }
    
    if priority == "medium":
        return {
            "rule_name": "warm_lead",
            **AUTOMATION_RULES["warm_lead"]
        }
    
    if priority == "low":
        return {
            "rule_name": "cold_lead",
            **AUTOMATION_RULES["cold_lead"]
        }
    
    # Default to warm lead if no specific match
    return {
        "rule_name": "warm_lead",
        **AUTOMATION_RULES["warm_lead"]
    }


def get_all_rules() -> Dict[str, Dict[str, Any]]:
    """Get all automation rules for documentation/admin purposes"""
    return AUTOMATION_RULES


def validate_rule(rule_name: str) -> bool:
    """Check if a rule exists"""
    return rule_name in AUTOMATION_RULES


def get_rule_by_name(rule_name: str) -> Dict[str, Any]:
    """Get a specific rule by name"""
    return AUTOMATION_RULES.get(rule_name, {})
