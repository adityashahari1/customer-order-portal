"""
Returns Processing Agent

Handles return requests, validates eligibility, and processes refunds.
"""

from backend.agents.agent_framework import BaseAgent
from backend.agents.tools.payment_tools import refund_payment
from backend.agents.tools.inventory_tools import update_inventory


def process_return(return_data: dict) -> dict:
    """
    Process a customer return request.
    
    Args:
        return_data: Dictionary containing:
            - return_id: int
            - order_id: int
            - customer_id: str
            - items: List[dict] with product_id and quantity
            - reason: str
            - charge_id: str (Stripe charge ID for refund)
            
    Returns:
        Dict with return processing results
    """
    # Create Returns Agent
    agent = BaseAgent(
        role='Returns Processing Specialist',
        goal='Process returns efficiently and ensure customer satisfaction',
        backstory="""You are an expert in handling returns and refunds.
        You validate return eligibility, process refunds, and update inventory accordingly.""",
        tools=[refund_payment, update_inventory],
        verbose=True,
        max_iterations=5
    )
    
    items_str = ", ".join([f"Product {item['product_id']}: {item['quantity']} units" 
                           for item in return_data.get('items', [])])
    
    task = f"""
    Process this return request:
    - Return ID: {return_data.get('return_id')}
    - Order ID: {return_data.get('order_id')}
    - Customer: {return_data.get('customer_id')}
    - Items: {items_str}
    - Reason: {return_data.get('reason', 'Not specified')}
    - Charge ID: {return_data.get('charge_id')}
    
    Steps:
    1. Process refund using refund_payment tool with charge_id={return_data.get('charge_id')}
    2. If refund succeeds, update inventory using update_inventory tool for each returned item (POSITIVE quantity_change to add back to stock)
    3. If refund fails, return 'REFUND_FAILED'
    4. If everything succeeds, return 'RETURN_COMPLETED'
    
    Final Answer should be either 'RETURN_COMPLETED' or 'REFUND_FAILED: [reason]'
    """
    
    result = agent.execute(task, context=return_data)
    
    # Parse result
    if "REFUND_FAILED" in result.upper() or "FAILED" in result.upper():
        return {
            "status": "REFUND_FAILED",
            "message": result,
            "return_id": return_data.get('return_id')
        }
    
    return {
        "status": "RETURN_COMPLETED",
        "message": f"Return {return_data.get('return_id')} processed successfully. Refund issued and inventory updated.",
        "return_id": return_data.get('return_id'),
        "details": result
    }
