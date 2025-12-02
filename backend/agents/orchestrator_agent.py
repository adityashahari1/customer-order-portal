"""
Orchestrator Agent

Routes customer queries to the appropriate specialist agents.
"""

from backend.agents.agent_framework import BaseAgent


def route_customer_query(query: str, customer_email: str) -> dict:
    """
    Analyze a customer query and route to the appropriate agent.
    
    Args:
        query: The customer's question or request
        customer_email: Customer's email address
        
    Returns:
        Dict with routing decision and recommended agent
    """
    # Create Orchestrator Agent without tools - relying on direct prompting
    agent = BaseAgent(
        role='Query Router and Customer Service Coordinator',
        goal='Analyze customer queries and route them to the appropriate specialist team',
        backstory="""You are an expert customer service coordinator with years of experience.
        You quickly analyze customer queries and determine which specialist team should handle them.
        You are decisive and efficient, always routing to the most appropriate specialist.""",
        tools=[], # No tools needed, just analysis
        verbose=True,
        max_iterations=1 # Simple classification task
    )
    
    task = f"""
    Analyze this customer query and determine the best specialist to handle it.
    
    Customer: {customer_email}
    Query: "{query}"
    
    Available specialists:
    1. ORDER: For "buy", "purchase", "place order", "new order", "where is my order", "status", "cancel".
    2. INVENTORY: For "stock", "availability", "do you have", "when will you have".
    3. RETURNS: ONLY for "return", "refund", "exchange", "defective", "broken".
    4. FRAUD: For "suspicious", "unauthorized", "hack", "security".
    5. SALESFORCE: For "update email", "change address", "crm", "account details".
    6. ESCALATION: For "manager", "supervisor", "complaint", "angry".
    
    Examples:
    - "I want to buy a laptop" -> ORDER
    - "Do you have stock?" -> INVENTORY
    - "I want to return this" -> RETURNS
    - "Where is my order?" -> ORDER
    
    INSTRUCTIONS:
    1. Analyze the intent of the query.
    2. Select exactly one specialist from the list above.
    3. Your Final Answer must be ONLY the specialist name in uppercase (e.g., "ORDER").
    """
    
    result = agent.execute(task, context={"query": query, "customer_email": customer_email})
    
    # Parse routing decision
    result_str = str(result).upper().strip()
    
    # Default to ORDER if unclear
    specialist = "ORDER"
    
    # Priority 1: Check for explicit "Final Answer: X" or "Specialist: X" patterns
    import re
    patterns = [
        r"FINAL ANSWER:?\s*(\w+)",
        r"SPECIALIST:?\s*(\w+)",
        r"SELECT:?\s*(\w+)",
        r"ROUTED TO:?\s*(\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, result_str)
        if match:
            found = match.group(1)
            if found in ["ORDER", "RETURNS", "INVENTORY", "FRAUD", "SALESFORCE", "ESCALATION"]:
                specialist = found
                break
    
    # Priority 2: If no pattern match, look for the words themselves (but be careful of "ORDER" appearing in "ORDER STATUS")
    if specialist == "ORDER":
        # Check for other specialists first (since ORDER is the default)
        if "RETURNS" in result_str or "RETURN" in result_str:
            specialist = "RETURNS"
        elif "INVENTORY" in result_str:
            specialist = "INVENTORY"
        elif "FRAUD" in result_str:
            specialist = "FRAUD"
        elif "SALESFORCE" in result_str:
            specialist = "SALESFORCE"
        elif "ESCALATION" in result_str:
            specialist = "ESCALATION"
        elif "ORDER" in result_str:
            specialist = "ORDER"
            
    # Priority 3: Fallback to keyword matching on the ORIGINAL query if the LLM was useless
    # This overrides the LLM if it made a clearly wrong choice (like sending "return" to "ORDER")
    query_lower = query.lower()
    
    # Strong keywords that should force a specific agent
    # Use word boundaries to avoid false matches (e.g., "return" shouldn't match "order")
    
    # Check SALESFORCE first (most specific keywords)
    if any(word in query_lower for word in ["update email", "change email", "update address", "change address", "update my email", "change my email", "crm", "account details", "update account", "change account"]):
        specialist = "SALESFORCE"
    elif any(word in query_lower for word in [" return ", "return ", " refund", "exchange", "send back", "send it back", "defective", "broken", "damaged", "not working", "doesn't work", "faulty"]):
        specialist = "RETURNS"
    elif any(word in query_lower for word in ["fraud", "unauthorized", "suspicious", "hacked", "stolen"]):
        specialist = "FRAUD"
    elif any(word in query_lower for word in [" stock", "available", "do you have", "in stock", "out of stock"]):
        specialist = "INVENTORY"
    elif any(word in query_lower for word in ["manager", "supervisor", "complain", "escalate", "speak to"]):
        specialist = "ESCALATION"
    elif any(word in query_lower for word in [" buy ", "purchase", " order ", "want to order", "place an order", "i want a", "i need a", "get a"]):
        specialist = "ORDER"
    
    return {
        "specialist": specialist,
        "query": query,
        "customer_email": customer_email,
        "message": f"I'll route your query to our {specialist} specialist who can help you best. They will assist you with: {query}"
    }

