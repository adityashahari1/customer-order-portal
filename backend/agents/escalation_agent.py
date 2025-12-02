"""
Escalation Agent

Handles customer escalations and creates high-priority support cases.
"""

from backend.agents.agent_framework import BaseAgent
from backend.agents.tools.salesforce_tools import create_salesforce_case


def escalate_issue(escalation_data: dict) -> dict:
    """
    Escalate a customer issue to management via Salesforce case.
    
    Args:
        escalation_data: Dictionary containing:
            - customer_email: str
            - issue_description: str
            - severity: str (Low, Medium, High, Critical)
            - customer_name: str (optional)
            
    Returns:
        Dict with escalation results
    """
    # Create Escalation Agent
    agent = BaseAgent(
        role='Customer Escalation Specialist',
        goal='Handle escalated issues and ensure timely resolution',
        backstory="""You are an expert in customer service escalations.
        You create high-priority cases and route critical issues to the appropriate teams.""",
        tools=[create_salesforce_case],
        verbose=True,
        max_iterations=3
    )
    
    severity = escalation_data.get('severity', 'High')
    task = f"""
    Escalate this customer issue:
    - Customer: {escalation_data.get('customer_email')}
    - Issue: {escalation_data.get('issue_description')}
    - Severity: {severity}
    
    Steps:
    1. Create a Salesforce case using create_salesforce_case tool
    2. Set priority to '{severity}' or 'High' if not specified
    3. Subject should be 'ESCALATION: {escalation_data.get('issue_description', '')[:50]}'
    4. Include full issue description
    
    Final Answer should confirm case creation with the case_id.
    """
    
    result = agent.execute(task, context=escalation_data)
    
    return {
        "status": "ESCALATED" if "success" in result.lower() or "case" in result.lower() else "ESCALATION_FAILED",
        "message": result,
        "customer_email": escalation_data.get('customer_email'),
        "severity": severity
    }
