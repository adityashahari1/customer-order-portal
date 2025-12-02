from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from simple_salesforce import Salesforce
import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from simple_salesforce import Salesforce
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def create_salesforce_case(
    customer_email: str,
    subject: str,
    description: str,
    priority: str = "Medium"
) -> dict:
    """Create a new case in Salesforce for customer support tracking.
    
    Args:
        customer_email: Customer's email address
        subject: Case subject/title
        description: Detailed description of the issue
        priority: Case priority (Low, Medium, or High). Defaults to Medium.
        
    Returns:
        Dict with status, case_id if successful, or error message
    """
    try:
        sf = Salesforce(
            username=os.getenv("SALESFORCE_USERNAME"),
            password=os.getenv("SALESFORCE_PASSWORD"),
            security_token=os.getenv("SALESFORCE_SECURITY_TOKEN")
        )
        
        case = sf.Case.create({
            'SuppliedEmail': customer_email,
            'Subject': subject,
            'Description': description,
            'Priority': priority,
            'Origin': 'Web',
            'Status': 'New'
        })
        
        return {
            "status": "success",
            "case_id": case['id'],
            "message": f"Case created successfully with ID: {case['id']}"
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
