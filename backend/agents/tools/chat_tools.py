"""
Chat-specific tools that wrap database operations for conversational agents.
These tools accept minimal input (like order_id) and look up necessary data from the database.
"""

from langchain_core.tools import tool
from backend.agents.tools.payment_tools import refund_payment
from backend.agents.tools.inventory_tools import check_inventory, update_inventory


@tool
def process_return_by_order_id(order_id: str, reason: str = "Customer request") -> dict:
    """Process a return for an order by looking up the order details.
    
    Args:
        order_id: The order ID (e.g., "1001" or "#1001")
        reason: Reason for return (optional)
        
    Returns:
        Dict with status and message
    """
    # Clean order_id (remove # if present)
    order_id_clean = order_id.replace("#", "").strip()
    
    # Mock database lookup (in production, this would query the actual database)
    # For demo purposes, we'll use mock data
    mock_orders = {
        "1001": {"charge_id": "ch_mock_1001", "amount": 129.99, "items": [{"product_id": 1, "quantity": 1}]},
        "1002": {"charge_id": "ch_mock_1002", "amount": 299.99, "items": [{"product_id": 2, "quantity": 1}]},
        "1005": {"charge_id": "ch_mock_1005", "amount": 89.99, "items": [{"product_id": 3, "quantity": 1}]},
    }
    
    if order_id_clean not in mock_orders:
        return {
            "status": "error",
            "message": f"Order #{order_id_clean} not found in our system. Please verify the order number."
        }
    
    order = mock_orders[order_id_clean]
    
    # Process refund
    refund_result = refund_payment(order["charge_id"])
    
    if refund_result.get("status") == "success":
        # Return items to inventory
        for item in order["items"]:
            update_inventory(
                product_id=item["product_id"],
                quantity_change=item["quantity"]  # Positive to add back
            )
        
        return {
            "status": "success",
            "message": f"Return processed successfully for order #{order_id_clean}. Refund of ${order['amount']:.2f} has been issued to your original payment method. You should see it in 3-5 business days.",
            "refund_amount": order["amount"]
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to process refund: {refund_result.get('error', 'Unknown error')}"
        }


@tool
def check_order_status(order_id: str) -> dict:
    """Look up the status of an order.
    
    Args:
        order_id: The order ID (e.g., "123" or "#123")
        
    Returns:
        Dict with order status and details
    """
    order_id_clean = order_id.replace("#", "").strip()
    
    # Mock database lookup
    mock_orders = {
        "123": {"status": "Shipped", "tracking": "TRACK123456", "eta": "2 days"},
        "1001": {"status": "Delivered", "tracking": "TRACK1001", "eta": "Delivered on Nov 15"},
        "1002": {"status": "Processing", "tracking": None, "eta": "Ships in 1-2 days"},
    }
    
    if order_id_clean not in mock_orders:
        return {
            "status": "not_found",
            "message": f"Order #{order_id_clean} not found. Please check the order number."
        }
    
    order = mock_orders[order_id_clean]
    
    message = f"Order #{order_id_clean} status: {order['status']}."
    if order['tracking']:
        message += f" Tracking: {order['tracking']}."
    if order['eta']:
        message += f" {order['eta']}."
    
    return {
        "status": "found",
        "message": message,
        "order_status": order['status'],
        "tracking": order.get('tracking'),
        "eta": order.get('eta')
    }


@tool
def check_product_stock(product_name: str) -> dict:
    """Check if a product is in stock.
    
    Args:
        product_name: Name or description of the product (e.g., "gaming laptop", "dell laptop")
        
    Returns:
        Dict with stock availability
    """
    product_lower = product_name.lower()
    
    # Mock product database
    mock_inventory = {
        "gaming laptop": {"product_id": 1, "stock": 15, "price": 1299.99, "name": "Gaming Laptop RTX 4060"},
        "dell laptop": {"product_id": 2, "stock": 8, "price": 899.99, "name": "Dell Latitude 15"},
        "mechanical keyboard": {"product_id": 3, "stock": 50, "price": 129.99, "name": "RGB Mechanical Keyboard"},
        "lenovo": {"product_id": 4, "stock": 0, "price": 1099.99, "name": "Lenovo ThinkPad"},
    }
    
    # Try to find matching product
    for key, product in mock_inventory.items():
        if key in product_lower or product_lower in key:
            if product["stock"] > 0:
                return {
                    "status": "in_stock",
                    "message": f"Yes! {product['name']} is in stock. We have {product['stock']} units available at ${product['price']:.2f}.",
                    "product_name": product['name'],
                    "stock": product['stock'],
                    "price": product['price']
                }
            else:
                return {
                    "status": "out_of_stock",
                    "message": f"Sorry, {product['name']} is currently out of stock. Would you like me to notify you when it's back in stock?",
                    "product_name": product['name']
                }
    
    return {
        "status": "not_found",
        "message": f"I couldn't find a product matching '{product_name}'. Could you provide more details or check the Inventory page for our full catalog?"
    }
