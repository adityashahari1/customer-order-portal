"""
Fraud Detection Agent

Analyzes transactions for suspicious patterns and potential fraud.
"""

from backend.agents.agent_framework import BaseAgent
from langchain_core.tools import tool


@tool
def analyze_transaction_pattern(
    customer_id: str,
    transaction_amount: float,
    transaction_count_24h: int
) -> dict:
    """Analyze transaction patterns for fraud detection.
    
    Args:
        customer_id: The customer's ID
        transaction_amount: Current transaction amount
        transaction_count_24h: Number of transactions in last 24 hours
        
    Returns:
        Dict with risk_score (0-100) and fraud indicators
    """
    risk_score = 0
    indicators = []
    
    # Check for suspicious patterns
    if transaction_amount > 1000:
        risk_score += 30
        indicators.append("High transaction amount")
    
    if transaction_count_24h > 10:
        risk_score += 40
        indicators.append("Unusual transaction frequency")
    
    if transaction_amount > 5000:
        risk_score += 30
        indicators.append("Very high transaction amount")
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "indicators": indicators,
        "recommendation": "BLOCK" if risk_score >= 70 else "REVIEW" if risk_score >= 40 else "APPROVE"
    }


def analyze_transaction(transaction_data: dict) -> dict:
    """
    Analyze a transaction for potential fraud.
    
    Args:
        transaction_data: Dictionary containing:
            - customer_id: str
            - transaction_amount: float
            - transaction_count_24h: int
            - customer_email: str
            
    Returns:
        Dict with fraud analysis results
    """
    # Create Fraud Detection Agent
    agent = BaseAgent(
        role='Fraud Detection Specialist',
        goal='Identify and prevent fraudulent transactions',
        backstory="""You are an expert in fraud detection and risk analysis.
        You analyze transaction patterns and customer behavior to identify suspicious activity.""",
        tools=[analyze_transaction_pattern],
        verbose=True,
        max_iterations=3
    )
    
    task = f"""
    Analyze this transaction for fraud:
    - Customer ID: {transaction_data.get('customer_id')}
    - Amount: ${transaction_data.get('transaction_amount')}
    - Recent transactions (24h): {transaction_data.get('transaction_count_24h', 0)}
    
    Steps:
    1. Use analyze_transaction_pattern tool with the transaction details
    2. Based on the risk_score and indicators, provide a final recommendation
    3. Return one of: 'APPROVED', 'FLAGGED_FOR_REVIEW', or 'BLOCKED'
    
    Final Answer should be the recommendation in uppercase.
    """
    
    result = agent.execute(task, context=transaction_data)
    
    # Parse result
    if "BLOCKED" in result.upper():
        status = "BLOCKED"
        message = "Transaction blocked due to high fraud risk"
    elif "REVIEW" in result.upper() or "FLAGGED" in result.upper():
        status = "FLAGGED_FOR_REVIEW"
        message = "Transaction flagged for manual review"
    else:
        status = "APPROVED"
        message = "Transaction approved"
    
    return {
        "status": status,
        "message": message,
        "analysis": result,
        "customer_id": transaction_data.get('customer_id')
    }
