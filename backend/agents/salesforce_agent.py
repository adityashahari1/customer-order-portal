"""
Salesforce Integration Agent

Syncs customer data and creates support cases in Salesforce.
"""

from backend.agents.agent_framework import BaseAgent
from backend.agents.tools.salesforce_tools import create_salesforce_case
from langchain_core.tools import tool
from simple_salesforce import Salesforce
import os


@tool
def sync_customer_to_salesforce(customer_email: str, customer_name: str) -> dict:
    """Sync customer information to Salesforce.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's full name
        
    Returns:
        Dict with sync status and contact_id if successful
    """
    try:
        sf = Salesforce(
            username=os.getenv("SALESFORCE_USERNAME"),
            password=os.getenv("SALESFORCE_PASSWORD"),
            security_token=os.getenv("SALESFORCE_SECURITY_TOKEN")
        )
        
        # Check if contact exists
        query = f"SELECT Id FROM Contact WHERE Email = '{customer_email}'"
        results = sf.query(query)
        
        if results['totalSize'] > 0:
            contact_id = results['records'][0]['Id']
            return {
                "status": "exists",
                "contact_id": contact_id,
                "message": "Customer already exists in Salesforce"
            }
        
        # Create new contact
        contact = sf.Contact.create({
            'Email': customer_email,
            'LastName': customer_name,
            'LeadSource': 'Web'
        })
        
        return {
            "status": "created",
            "contact_id": contact['id'],
            "message": f"Customer synced to Salesforce with ID: {contact['id']}"
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


def sync_customer_data(customer_data: dict) -> dict:
    """
    Sync customer data to Salesforce.
    
    Args:
        customer_data: Dictionary containing customer_email and customer_name
        
    Returns:
        Dict with sync results
    """
    agent = BaseAgent(
        role='Salesforce Integration Specialist',
        goal='Keep customer data synchronized with Salesforce CRM',
        backstory="""You are an expert in CRM integration and data synchronization.
        You ensure customer information is accurately maintained in Salesforce.""",
        tools=[sync_customer_to_salesforce, create_salesforce_case],
        verbose=True,
        max_iterations=3
    )
    
    task = f"""
    Sync customer to Salesforce:
    - Email: {customer_data.get('customer_email')}
    - Name: {customer_data.get('customer_name')}
    
    Use sync_customer_to_salesforce tool to create or update the customer record.
    
    Final Answer should indicate whether sync was successful and the contact_id.
    """
    
    result = agent.execute(task, context=customer_data)
    
    return {
        "status": "SYNCED" if "success" in result.lower() or "created" in result.lower() or "exists" in result.lower() else "SYNC_FAILED",
        "message": result,
        "customer_email": customer_data.get('customer_email')
    }
