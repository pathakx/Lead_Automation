from groq import Groq
from typing import Dict, Any, Optional
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AIService:
    """
    Production-ready AI service with:
    - Versioning for auditability
    - Fallback categorization
    - Retry logic
    - Error handling
    """
    
    MODEL_VERSION = "llama-3.3-70b-versatile"  # Updated to current model
    PROMPT_VERSION = "v1.1"  # Enhanced with detailed rules and examples
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    async def categorize_lead(
        self, 
        lead_data: Dict[str, Any],
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """
        Categorize lead using AI with fallback
        
        Returns dict with:
        - input: original lead data (for replay)
        - output: AI categorization
        - model: model version used
        - prompt_version: prompt version used
        - method: 'ai' or 'fallback'
        - timestamp: when categorization happened
        """
        
        # Store original input for replay capability
        lead_input = {
            "role": lead_data.get('role'),
            "location": lead_data.get('location'),
            "products": lead_data.get('products', []),
            "message": lead_data.get('message')
        }
        
        # Try AI categorization with retries
        for attempt in range(retry_count):
            try:
                result = await self._call_groq_api(lead_input)
                
                return {
                    "input": lead_input,
                    "output": result,
                    "model": self.MODEL_VERSION,
                    "prompt_version": self.PROMPT_VERSION,
                    "method": "ai",
                    "timestamp": datetime.utcnow().isoformat(),
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                logger.warning(f"AI categorization attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    continue  # Retry
                else:
                    # All retries failed, use fallback
                    logger.error(f"All AI attempts failed, using fallback for lead")
                    return self.fallback_categorization(lead_input)
    
    async def _call_groq_api(self, lead_input: Dict) -> Dict:
        """Make actual Groq API call with enhanced prompt"""
        
        prompt = f"""Analyze this lead inquiry and categorize it accurately.

LEAD INFORMATION:
- Role: {lead_input.get('role', 'Unknown')}
- Location: {lead_input.get('location', 'Unknown')}
- Products of Interest: {', '.join(lead_input.get('products', []))}
- Message: {lead_input.get('message', 'No message')}

CATEGORIZATION RULES:

1. PRIORITY (high/medium/low):
   - HIGH: 
     * Architects or Builders (professional buyers)
     * Urgent requests (contains: urgent, ASAP, immediately, today)
     * Bulk orders or large projects (mentions: bulk, project, commercial, 50+ units)
     * Quote requests with specific quantities
   - MEDIUM: 
     * Contractors with specific inquiries
     * Home owners requesting quotes
     * Specific product inquiries with timeline
   - LOW: 
     * General browsing or information requests
     * Home owners just looking/exploring
     * Price comparison without commitment

2. INTENT (quote_request/information/complaint/partnership):
   - quote_request: Mentions pricing, quote, estimate, bulk, project, need materials
   - information: Just looking, browsing, learning, exploring, what types
   - complaint: Issues, problems, dissatisfaction, not working
   - partnership: Business collaboration, dealer inquiry, distribution

3. LEAD_TYPE (architect/builder/contractor/homeowner):
   - architect: Role is "Architect"
   - builder: Role is "Builder"  
   - contractor: Role is "Contractor"
   - homeowner: Role is "Home Owner" (note the space and capitalization)

4. SUGGESTED_ACTIONS (array of strings):
   Choose from: ["call", "email", "send_quote", "schedule_demo", "nurture"]
   - High priority: ["call", "send_quote"]
   - Medium priority: ["email", "send_quote"]
   - Low priority: ["nurture", "email"]

EXAMPLES:

Example 1:
Input: Architect, "Need urgent quote for 5000 sq ft luxury project"
Output: {{"priority": "high", "intent": "quote_request", "lead_type": "architect", "suggested_actions": ["call", "send_quote"]}}

Example 2:
Input: Home Owner, "Just looking at flooring options"
Output: {{"priority": "low", "intent": "information", "lead_type": "homeowner", "suggested_actions": ["nurture", "email"]}}

Example 3:
Input: Builder, "Bulk pricing for 50 unit residential complex"
Output: {{"priority": "high", "intent": "quote_request", "lead_type": "builder", "suggested_actions": ["call", "send_quote"]}}

RESPOND IN THIS EXACT JSON FORMAT (no additional text):
{{
    "priority": "high|medium|low",
    "intent": "quote_request|information|complaint|partnership",
    "lead_type": "architect|builder|contractor|homeowner",
    "suggested_actions": ["action1", "action2"],
    "reasoning": "Brief explanation of categorization"
}}

IMPORTANT: 
- Use lowercase for all values except in reasoning
- lead_type must be exactly: architect, builder, contractor, or homeowner
- Respond ONLY with valid JSON, no markdown formatting
"""
        
        response = self.client.chat.completions.create(
            model=self.MODEL_VERSION,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
            timeout=30  # 30 second timeout
        )
        
        return json.loads(response.choices[0].message.content)
    
    def fallback_categorization(self, lead_input: Dict) -> Dict:
        """
        Simple rule-based fallback when AI fails
        Uses keyword matching and heuristics
        """
        
        message = (lead_input.get('message') or '').lower()
        role = (lead_input.get('role') or '').lower()
        
        # Determine priority based on keywords
        urgent_keywords = ["urgent", "asap", "immediately", "need now", "today"]
        quote_keywords = ["quote", "price", "cost", "budget", "estimate"]
        
        is_urgent = any(kw in message for kw in urgent_keywords)
        wants_quote = any(kw in message for kw in quote_keywords)
        
        if is_urgent or wants_quote:
            priority = "high"
            suggested_action = "call_within_30_min"
            intent = "quote_request"
        else:
            priority = "medium"
            suggested_action = "email_response"
            intent = "product_info"
        
        # Map role to lead_type
        lead_type_map = {
            "home owner": "home_owner",
            "architect": "architect",
            "builder": "builder",
            "contractor": "contractor"
        }
        lead_type = lead_type_map.get(role, "home_owner")
        
        return {
            "input": lead_input,
            "output": {
                "intent": intent,
                "lead_type": lead_type,
                "priority": priority,
                "suggested_action": suggested_action,
                "reasoning": "Fallback rule-based categorization (AI unavailable)"
            },
            "model": "rule_based_fallback",
            "prompt_version": "N/A",
            "method": "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }


# Initialize AI service (singleton)
ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        from app.config import settings
        ai_service = AIService(api_key=settings.GROQ_API_KEY)
    return ai_service
