import pytest
from app.config.automation_rules import (
    get_matching_rule,
    get_all_rules,
    validate_rule,
    get_rule_by_name,
    AUTOMATION_RULES
)


# ============================================================================
# Test: Rule Matching - High Priority
# ============================================================================

def test_get_matching_rule_architect_vip():
    """Test architect VIP rule matching (high priority + architect)"""
    ai_result = {
        "priority": "high",
        "intent": "quote_request",
        "lead_type": "architect"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "architect_vip"
    assert "actions" in rule
    assert len(rule["actions"]) > 0
    
    # Verify VIP-specific actions
    action_types = [action["type"] for action in rule["actions"]]
    assert "send_email" in action_types
    assert "create_follow_up" in action_types


def test_get_matching_rule_builder_bulk():
    """Test builder bulk rule matching (high priority + builder)"""
    ai_result = {
        "priority": "high",
        "intent": "quote_request",
        "lead_type": "builder"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "builder_bulk"
    assert "actions" in rule


def test_get_matching_rule_hot_lead():
    """Test hot lead rule matching (high priority + quote request)"""
    ai_result = {
        "priority": "high",
        "intent": "quote_request",
        "lead_type": "contractor"  # Not architect or builder
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "hot_lead"
    assert rule["criteria"]["priority"] == "high"
    assert rule["criteria"]["intent"] == "quote_request"


# ============================================================================
# Test: Rule Matching - Medium Priority
# ============================================================================

def test_get_matching_rule_warm_lead():
    """Test warm lead rule matching (medium priority)"""
    ai_result = {
        "priority": "medium",
        "intent": "quote_request",
        "lead_type": "homeowner"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "warm_lead"
    assert rule["criteria"]["priority"] == "medium"


def test_get_matching_rule_medium_priority_contractor():
    """Test medium priority contractor gets warm lead workflow"""
    ai_result = {
        "priority": "medium",
        "intent": "information",
        "lead_type": "contractor"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "warm_lead"


# ============================================================================
# Test: Rule Matching - Low Priority
# ============================================================================

def test_get_matching_rule_cold_lead():
    """Test cold lead rule matching (low priority)"""
    ai_result = {
        "priority": "low",
        "intent": "information",
        "lead_type": "homeowner"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "cold_lead"
    assert rule["criteria"]["priority"] == "low"


# ============================================================================
# Test: Rule Matching - Partnership
# ============================================================================

def test_get_matching_rule_partnership():
    """Test partnership inquiry rule matching"""
    ai_result = {
        "priority": "medium",
        "intent": "partnership",
        "lead_type": "contractor"
    }
    
    rule = get_matching_rule(ai_result)
    
    assert rule["rule_name"] == "partnership_inquiry"
    assert rule["criteria"]["intent"] == "partnership"


def test_get_matching_rule_partnership_high_priority():
    """Test partnership takes precedence even with high priority"""
    ai_result = {
        "priority": "high",
        "intent": "partnership",
        "lead_type": "builder"
    }
    
    rule = get_matching_rule(ai_result)
    
    # Builder + high + partnership should match builder_bulk (specific combo takes precedence)
    assert rule["rule_name"] == "builder_bulk"


# ============================================================================
# Test: Rule Matching - Edge Cases
# ============================================================================

def test_get_matching_rule_default_fallback():
    """Test default fallback to warm lead for unmatched scenarios"""
    ai_result = {
        "priority": "unknown",
        "intent": "other",
        "lead_type": "unknown"
    }
    
    rule = get_matching_rule(ai_result)
    
    # Should default to warm_lead
    assert rule["rule_name"] == "warm_lead"


def test_get_matching_rule_architect_low_priority():
    """Test architect with low priority doesn't trigger VIP workflow"""
    ai_result = {
        "priority": "low",
        "intent": "information",
        "lead_type": "architect"
    }
    
    rule = get_matching_rule(ai_result)
    
    # Should match cold_lead, not architect_vip
    assert rule["rule_name"] == "cold_lead"


def test_get_matching_rule_builder_medium_priority():
    """Test builder with medium priority doesn't trigger bulk workflow"""
    ai_result = {
        "priority": "medium",
        "intent": "information",
        "lead_type": "builder"
    }
    
    rule = get_matching_rule(ai_result)
    
    # Should match warm_lead, not builder_bulk
    assert rule["rule_name"] == "warm_lead"


# ============================================================================
# Test: Rule Actions Validation
# ============================================================================

def test_architect_vip_rule_actions():
    """Test architect VIP rule has correct actions"""
    rule = AUTOMATION_RULES["architect_vip"]
    
    action_types = [action["type"] for action in rule["actions"]]
    
    # Should have email, follow-up, approval, assignment
    assert "send_email" in action_types
    assert "create_follow_up" in action_types
    assert "create_approval" in action_types
    assert "create_assignment" in action_types
    
    # Check for VIP-specific actions
    has_notify = any(action["type"] == "notify_sales" for action in rule["actions"])
    assert has_notify  # Should notify sales team


def test_hot_lead_rule_actions():
    """Test hot lead rule has correct actions"""
    rule = AUTOMATION_RULES["hot_lead"]
    
    action_types = [action["type"] for action in rule["actions"]]
    
    assert "send_email" in action_types
    assert "create_follow_up" in action_types
    assert "create_assignment" in action_types
    assert "create_approval" in action_types


def test_warm_lead_rule_actions():
    """Test warm lead rule has correct actions"""
    rule = AUTOMATION_RULES["warm_lead"]
    
    action_types = [action["type"] for action in rule["actions"]]
    
    # Should have multiple emails (acknowledgement + nurture)
    email_actions = [a for a in rule["actions"] if a["type"] == "send_email"]
    assert len(email_actions) >= 2  # At least 2 emails


def test_cold_lead_rule_actions():
    """Test cold lead rule has correct actions"""
    rule = AUTOMATION_RULES["cold_lead"]
    
    action_types = [action["type"] for action in rule["actions"]]
    
    assert "send_email" in action_types
    assert "create_follow_up" in action_types
    assert "create_assignment" in action_types


# ============================================================================
# Test: SLA Hours Validation
# ============================================================================

def test_architect_vip_sla_hours():
    """Test architect VIP has 1 hour SLA"""
    rule = AUTOMATION_RULES["architect_vip"]
    
    assignment_action = next(
        (a for a in rule["actions"] if a["type"] == "create_assignment"),
        None
    )
    
    assert assignment_action is not None
    assert assignment_action["sla_hours"] == 1


def test_hot_lead_sla_hours():
    """Test hot lead has 1 hour SLA"""
    rule = AUTOMATION_RULES["hot_lead"]
    
    assignment_action = next(
        (a for a in rule["actions"] if a["type"] == "create_assignment"),
        None
    )
    
    assert assignment_action is not None
    assert assignment_action["sla_hours"] == 1


def test_warm_lead_sla_hours():
    """Test warm lead has 24 hour SLA"""
    rule = AUTOMATION_RULES["warm_lead"]
    
    assignment_action = next(
        (a for a in rule["actions"] if a["type"] == "create_assignment"),
        None
    )
    
    assert assignment_action is not None
    assert assignment_action["sla_hours"] == 24


def test_cold_lead_sla_hours():
    """Test cold lead has 72 hour SLA"""
    rule = AUTOMATION_RULES["cold_lead"]
    
    assignment_action = next(
        (a for a in rule["actions"] if a["type"] == "create_assignment"),
        None
    )
    
    assert assignment_action is not None
    assert assignment_action["sla_hours"] == 72


# ============================================================================
# Test: Email Template Validation
# ============================================================================

def test_architect_vip_uses_high_priority_template():
    """Test architect VIP uses high-priority email template"""
    rule = AUTOMATION_RULES["architect_vip"]
    
    email_action = next(
        (a for a in rule["actions"] if a["type"] == "send_email"),
        None
    )
    
    assert email_action is not None
    assert email_action["template"] == "immediate_response_high_priority"


def test_warm_lead_email_templates():
    """Test warm lead uses correct email templates"""
    rule = AUTOMATION_RULES["warm_lead"]
    
    email_actions = [a for a in rule["actions"] if a["type"] == "send_email"]
    
    templates = [a["template"] for a in email_actions]
    
    # Should have acknowledgement and nurture
    assert "acknowledgement" in templates
    assert "nurture_day_0" in templates


# ============================================================================
# Test: Utility Functions
# ============================================================================

def test_get_all_rules():
    """Test get_all_rules returns all automation rules"""
    all_rules = get_all_rules()
    
    assert isinstance(all_rules, dict)
    assert len(all_rules) == 6  # 6 workflow types
    
    # Verify all expected rules exist
    expected_rules = [
        "hot_lead",
        "warm_lead",
        "cold_lead",
        "architect_vip",
        "builder_bulk",
        "partnership_inquiry"
    ]
    
    for rule_name in expected_rules:
        assert rule_name in all_rules


def test_validate_rule_existing():
    """Test validate_rule returns True for existing rules"""
    assert validate_rule("hot_lead") is True
    assert validate_rule("warm_lead") is True
    assert validate_rule("cold_lead") is True
    assert validate_rule("architect_vip") is True
    assert validate_rule("builder_bulk") is True
    assert validate_rule("partnership_inquiry") is True


def test_validate_rule_nonexistent():
    """Test validate_rule returns False for non-existent rules"""
    assert validate_rule("nonexistent_rule") is False
    assert validate_rule("invalid_rule") is False
    assert validate_rule("") is False


def test_get_rule_by_name_existing():
    """Test get_rule_by_name returns correct rule"""
    rule = get_rule_by_name("hot_lead")
    
    assert rule is not None
    assert "description" in rule
    assert "criteria" in rule
    assert "actions" in rule


def test_get_rule_by_name_nonexistent():
    """Test get_rule_by_name returns empty dict for non-existent rule"""
    rule = get_rule_by_name("nonexistent_rule")
    
    assert rule == {}


# ============================================================================
# Test: Rule Priority Order
# ============================================================================

def test_rule_matching_priority_order():
    """Test that specific combinations take precedence over general rules"""
    
    # Architect + high should match architect_vip, not hot_lead
    ai_result_1 = {
        "priority": "high",
        "intent": "quote_request",
        "lead_type": "architect"
    }
    rule_1 = get_matching_rule(ai_result_1)
    assert rule_1["rule_name"] == "architect_vip"
    
    # Builder + high should match builder_bulk, not hot_lead
    ai_result_2 = {
        "priority": "high",
        "intent": "quote_request",
        "lead_type": "builder"
    }
    rule_2 = get_matching_rule(ai_result_2)
    assert rule_2["rule_name"] == "builder_bulk"
    
    # Architect + high + partnership should still match architect_vip (specific combo takes precedence)
    ai_result_3 = {
        "priority": "high",
        "intent": "partnership",
        "lead_type": "architect"
    }
    rule_3 = get_matching_rule(ai_result_3)
    assert rule_3["rule_name"] == "architect_vip"  # Specific combination takes precedence


# ============================================================================
# Test: Rule Descriptions
# ============================================================================

def test_all_rules_have_descriptions():
    """Test that all rules have descriptions"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        assert "description" in rule
        assert len(rule["description"]) > 0


def test_all_rules_have_criteria():
    """Test that all rules have criteria"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        assert "criteria" in rule
        assert isinstance(rule["criteria"], dict)


def test_all_rules_have_actions():
    """Test that all rules have actions"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        assert "actions" in rule
        assert isinstance(rule["actions"], list)
        assert len(rule["actions"]) > 0


# ============================================================================
# Test: Action Structure Validation
# ============================================================================

def test_all_actions_have_required_fields():
    """Test that all actions have required fields"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        for action in rule["actions"]:
            # Every action must have a type
            assert "type" in action
            assert len(action["type"]) > 0
            
            # Every action should have a description
            assert "description" in action


def test_email_actions_have_templates():
    """Test that email actions have template specified"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        for action in rule["actions"]:
            if action["type"] == "send_email":
                assert "template" in action
                assert len(action["template"]) > 0


def test_assignment_actions_have_owner_and_sla():
    """Test that assignment actions have owner and SLA"""
    all_rules = get_all_rules()
    
    for rule_name, rule in all_rules.items():
        for action in rule["actions"]:
            if action["type"] == "create_assignment":
                assert "owner" in action
                assert "sla_hours" in action
                assert isinstance(action["sla_hours"], int)
                assert action["sla_hours"] > 0
