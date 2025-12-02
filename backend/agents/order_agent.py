"""
Order Processing Agent

Handles new order validation, inventory checks, and payment processing.
"""

from backend.agents.agent_framework import BaseAgent
from backend.agents.tools.inventory_tools import check_inventory, update_inventory
from backend.agents.tools.payment_tools import process_payment


def process_new_order(order_data: dict) -> dict:
    """
    Process a new customer order.
    
    Args:
        order_data: Dictionary containing:
            - order_id: int
            - customer_id: str
            - items: List[dict] with product_id and quantity
            - total_amount: float
            
    Returns:
        Dict with status and message
    """
    # Create Order Processing Agent
    agent = BaseAgent(
        role='Order Processing Specialist',
        goal='Validate orders, check inventory, and process payments efficiently',
        backstory="""You are an expert in order fulfillment. 
        You ensure that every order is valid, items are in stock, and payments are secured before confirming an order.""",
        tools=[check_inventory, update_inventory, process_payment],
        verbose=True,
        max_iterations=5
    )
    
    # Step 1: Check inventory for all items
    items_str = ", ".join([f"Product {item['product_id']}: {item['quantity']} units" 
                           for item in order_data.get('items', [])])
    
    inventory_task = f"""
    Check inventory for these items: {items_str}.
    
    For EACH product:
    1. Use check_inventory tool to verify stock availability
    2. If ANY item is out of stock, immediately return 'OUT_OF_STOCK: [product_id]'
    3. If ALL items are in stock, proceed to reserve them by updating inventory
    
    Use update_inventory with NEGATIVE quantity_change to reserve stock for the order.
    
    Final Answer should be either:
    - 'OUT_OF_STOCK: [product_id]' if any item lacks stock
    - 'STOCK_RESERVED' if all items successfully reserved
    """
    
    inventory_result = agent.execute(inventory_task, context=order_data)
    
    # Check if out of stock
    if "OUT_OF_STOCK" in inventory_result:
        return {
            "status": "OUT_OF_STOCK",
            "message": inventory_result,
            "order_id": order_data.get('order_id')
        }
    
    # Step 2: Process payment
    payment_task = f"""
    Process payment for order total of ${order_data.get('total_amount', 0)}.
    
    Steps:
    1. Use process_payment tool with amount={order_data.get('total_amount')} and customer_id={order_data.get('customer_id')}
    2. If payment succeeds, return 'PAYMENT_SUCCESS'
    3. If payment fails, return 'PAYMENT_FAILED: [error details]'
    
    Final Answer should be either:
    - 'PAYMENT_SUCCESS' if payment processed
    - 'PAYMENT_FAILED: [reason]' if payment failed
    """
    
    payment_result = agent.execute(payment_task, context=order_data)
    
    # Check if payment failed
    if "PAYMENT_FAILED" in payment_result or "failed" in payment_result.lower():
        # Rollback inventory reservation
        rollback_task = "Release the reserved inventory by updating stock back (positive quantity_change)"
        agent.execute(rollback_task)
        
        return {
            "status": "PAYMENT_FAILED",
            "message": payment_result,
            "order_id": order_data.get('order_id')
        }
    
    # Success!
    return {
        "status": "ORDER_CONFIRMED",
        "message": f"Order {order_data.get('order_id')} confirmed successfully. Payment processed and inventory reserved.",
        "order_id": order_data.get('order_id'),
        "payment_details": payment_result
    }
