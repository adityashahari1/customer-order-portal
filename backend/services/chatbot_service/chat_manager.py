# -*- coding: utf-8 -*-
from backend.agents.orchestrator_agent import route_customer_query
import logging
import re
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

# Simple in-memory history (in production this should be in Redis)
conversation_history = {}

# Pending order confirmations: {user_email: {'product': item, 'timestamp': datetime}}
pending_orders = {}

# Backend service URLs
GATEWAY_URL = "http://localhost:8000/api"

async def process_message(message: str, user_email: str) -> str:
    """Process chat message through the orchestrator and specialist agents"""
    try:
        # Get history
        if user_email not in conversation_history:
            conversation_history[user_email] = []
            
        # Add user message to history
        conversation_history[user_email].append(f"Customer: {message}")
        
        # Keep only last 5 interactions to avoid context limit
        if len(conversation_history[user_email]) > 10:
            conversation_history[user_email] = conversation_history[user_email][-10:]
            
        history_str = "\n".join(conversation_history[user_email])

        # IMPORTANT: Check for pending order confirmations BEFORE routing
        # This prevents "yes"/"no" responses from being misrouted by orchestrator
        message_lower = message.lower().strip()
        confirmation_keywords = ["yes", "confirm", "place order", "order it", "sure", "ok", "okay", "proceed"]
        cancellation_keywords = ["no", "cancel", "nevermind", "never mind", "changed my mind"]
        
        is_confirmation = any(keyword == message_lower or keyword in message_lower for keyword in confirmation_keywords)
        is_cancellation = any(keyword == message_lower or keyword in message_lower for keyword in cancellation_keywords)
        
        # If user has pending order and is confirming/cancelling, route directly to ORDER specialist
        if (is_confirmation or is_cancellation) and user_email in pending_orders:
            specialist = "ORDER"
            logger.info(f"Pending order detected - routing '{message}' directly to ORDER specialist")
        else:
            # 1. Route the query via orchestrator
            routing_result = route_customer_query(message, user_email)
            
            if not isinstance(routing_result, dict):
                return str(routing_result)
                
            specialist = routing_result.get('specialist', 'ORDER')
            logger.info(f"Routing query '{message}' to {specialist}")
        
        # 2. Process based on specialist type with REAL API calls
        response = await process_with_real_services(specialist, message, history_str, user_email)
        
        # Add agent response to history
        conversation_history[user_email].append(f"Agent: {response}")
            
        return response

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return f"I apologize, but I encountered an error. Please try again or contact support."

async def process_with_real_services(specialist: str, message: str, history: str, user_email: str) -> str:
    """Process message by calling real backend services"""
    
    message_lower = message.lower()
    
    # Extract order ID - ONLY from current message, not history
    # This prevents SKUs (like "GLAP-4060") from being treated as order IDs
    order_match = re.search(r'(?:order\s*#?\s*|#)(\d{3,5})', message, re.IGNORECASE)
    order_id = order_match.group(1) if order_match else None
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        if specialist == "RETURNS":
            if order_id:
                try:
                    # Call the real returns service API
                    response = await client.post(
                        f"{GATEWAY_URL}/returns/",
                        json={
                            "order_id": int(order_id),
                            "reason": "Customer request via chat",
                            "refund_amount": 0.0  # Will be calculated by backend
                        },
                        headers={"Authorization": "Bearer mock-token-for-testing"}
                    )
                    
                    if response.status_code == 200 or response.status_code == 201:
                        data = response.json()
                        return f"""✅ I've successfully processed your return for order #{order_id}.

**Return Details:**
• Return ID: #{data.get('id', 'N/A')}
• Status: {data.get('status', 'Pending').title()}
• Reason: {data.get('reason', 'Customer request')}

Your refund will be processed within 3-5 business days and credited to your original payment method.

Is there anything else I can help you with?"""
                    else:
                        return f"I encountered an issue processing the return for order #{order_id}. Please try again or contact support."
                        
                except Exception as e:
                    logger.error(f"Error calling returns API: {e}")
                    return f"I'm having trouble connecting to our returns system. Please try again in a moment or contact support."
            else:
                return "I'd be happy to help you process a return. Could you please provide your order number? (e.g., #1001)"
        
        elif specialist == "ORDER":
            # Check for confirmation keywords first (yes/no for pending orders)
            confirmation_keywords = ["yes", "confirm", "place order", "order it", "sure", "ok", "okay", "proceed"]
            cancellation_keywords = ["no", "cancel", "nevermind", "never mind", "changed my mind"]
            
            is_confirmation = any(keyword in message_lower for keyword in confirmation_keywords)
            is_cancellation = any(keyword in message_lower for keyword in cancellation_keywords)
            
            # Handle confirmation for pending order
            if is_confirmation and user_email in pending_orders:
                pending = pending_orders[user_email]
                product = pending['product']
                
                try:
                    # Create order via Order Service API
                    order_payload = {
                        "user_id": 1,  # Mock user_id (in production, lookup from Customer Service)
                        "total_amount": product['price'],
                        "items": [{
                            "product_id": product['id'],
                            "quantity": 1,
                            "price": product['price']
                        }]
                    }
                    
                    response = await client.post(
                        f"{GATEWAY_URL}/orders/",
                        json=order_payload
                    )
                    
                    if response.status_code in [200, 201]:
                        order_data = response.json()
                        order_id = order_data.get('id', 'N/A')
                        
                        # Clear pending order
                        del pending_orders[user_email]
                        
                        return f"""✅ **Order Confirmed!**

**Order Details:**
• Order ID: #{order_id}
• Product: {product['name']}
• Price: ${product['price']:.2f}
• Status: Processing

Your order is being prepared for shipment. You'll receive a confirmation email shortly!

Is there anything else I can help you with?"""
                    else:
                        return f"I encountered an issue creating your order. Please try again or contact support. Error: {response.status_code}"
                        
                except Exception as e:
                    logger.error(f"Error creating order: {e}")
                    return "I'm having trouble creating your order. Please try again in a moment or contact support."
            
            # Handle cancellation of pending order
            elif is_cancellation and user_email in pending_orders:
                del pending_orders[user_email]
                return "No problem! I've cancelled that order request. Let me know if you'd like to order something else."
            
            # Check if this is a purchase intent vs order tracking
            purchase_keywords = [
                "buy", "purchase", "order a", "place an order", "place order",
                "get a", "want a", "need a", "i want to order", "i want to buy",
                "i want to purchase", "i'd like to order", "i'd like to buy",
                "can i order", "can i buy", "looking to buy", "looking to order"
            ]
            is_purchase = any(keyword in message_lower for keyword in purchase_keywords)
            
            # If there's an order ID mentioned, it's likely tracking (unless they say "order a <product>")
            if order_id and not is_purchase:
                tracking_mode = True
            else:
                tracking_mode = False
            
            if is_purchase and not tracking_mode:
                # Customer wants to make a new purchase - search inventory
                try:
                    response = await client.get(f"{GATEWAY_URL}/inventory/")
                    
                    if response.status_code == 200:
                        inventory_items = response.json()
                        
                        # Extract product keywords from message
                        product_keywords = ["laptop", "keyboard", "mouse", "monitor", "gaming", "thinkpad", "dell", "lenovo", "rtx"]
                        mentioned_keywords = [kw for kw in product_keywords if kw in message_lower]
                        
                        if mentioned_keywords:
                            # Search for matching product
                            matching_items = []
                            for item in inventory_items:
                                item_name_lower = item.get('name', '').lower()
                                # Check if any mentioned keyword is in the product name
                                if any(kw in item_name_lower for kw in mentioned_keywords):
                                    matching_items.append(item)
                            
                            if matching_items:
                                # Take first matching product
                                product = matching_items[0]
                                stock = product.get('stock', 0)
                                
                                if stock > 0:
                                    # Store pending order
                                    pending_orders[user_email] = {
                                        'product': product,
                                        'timestamp': datetime.now()
                                    }
                                    
                                    return f"""✅ Great! I found **{product['name']}** in our inventory.

**Product Details:**
• Price: ${product['price']:.2f}
• In Stock: {stock} units available
• SKU: {product.get('sku', 'N/A')}

Reply **'yes'** to place this order, or **'no'** to cancel."""
                                else:
                                    return f"❌ Sorry, **{product['name']}** is currently out of stock. Would you like me to notify you when it's back in stock?"
                            else:
                                # No matching products found
                                available_products = "\n".join([f"• {item.get('name')} - ${item.get('price', 0):.2f}" for item in inventory_items[:5]])
                                return f"""I couldn't find a product matching your search. Here are some available products:

{available_products}

What would you like to order?"""
                        else:
                            # No keywords mentioned - show general options
                            available_products = "\n".join([f"• {item.get('name')} - ${item.get('price', 0):.2f}" for item in inventory_items[:5]])
                            return f"""I'd be happy to help you place an order!

**Available Products:**
{available_products}

What would you like to order?"""
                    else:
                        return "I'm having trouble checking our inventory. Please try again in a moment."
                        
                except Exception as e:
                    logger.error(f"Error searching inventory: {e}")
                    return "I'm having trouble connecting to our inventory system. Please try again."
            
            elif tracking_mode:
                try:
                    # Call the real order service API
                    response = await client.get(f"{GATEWAY_URL}/orders/{order_id}")
                    
                    if response.status_code == 200:
                        order = response.json()
                        status = order.get('status', 'Unknown')
                        total = order.get('total_amount', 0)
                        
                        return f"""📦 **Order #{order_id}** - Status: **{status}**

• Total Amount: ${total:.2f}
• Order Date: {order.get('created_at', 'N/A')}

{get_status_message(status)}

Need help with anything else?"""
                    elif response.status_code == 404:
                        return f"I couldn't find order #{order_id} in our system. Please double-check the order number."
                    else:
                        return f"I'm having trouble looking up that order. Please try again."
                        
                except Exception as e:
                    logger.error(f"Error calling order API: {e}")
                    return "I'm having trouble connecting to our order system. Please try again in a moment."
            else:
                return "I can help you track your order! Please provide your order number (e.g., #123)."
        
        elif specialist == "INVENTORY":
            # Extract product name from message
            product_keywords = ["laptop", "keyboard", "lenovo", "dell", "gaming", "thinkpad"]
            product_name = None
            for keyword in product_keywords:
                if keyword in message_lower:
                    product_name = keyword
                    break
            
            if product_name:
                try:
                    # Call the real inventory service API
                    response = await client.get(f"{GATEWAY_URL}/inventory/")
                    
                    if response.status_code == 200:
                        inventory_items = response.json()
                        
                        # Find matching product
                        matching_items = [
                            item for item in inventory_items 
                            if product_name.lower() in item.get('name', '').lower()
                        ]
                        
                        if matching_items:
                            item = matching_items[0]
                            stock = item.get('stock', 0)
                            price = item.get('price', 0)
                            name = item.get('name', 'Product')
                            
                            if stock > 0:
                                return f"""✅ Yes! **{name}** is in stock!

• Available: {stock} units
• Price: ${price:.2f}
• SKU: {item.get('sku', 'N/A')}

Would you like to place an order?"""
                            else:
                                return f"❌ Sorry, **{name}** is currently out of stock. Would you like me to notify you when it's back?"
                        else:
                            return f"I couldn't find a product matching '{product_name}'. Could you be more specific?"
                    else:
                        return "I'm having trouble checking inventory right now. Please try again."
                        
                except Exception as e:
                    logger.error(f"Error calling inventory API: {e}")
                    return "I'm having trouble connecting to our inventory system. Please try again."
            else:
                return "I can help you check product availability. What are you looking for? (e.g., gaming laptop, keyboard)"
        
        elif specialist == "FRAUD":
            return """🚨 **Security Alert**

I take this very seriously. Here's what you should do **immediately**:

1. 🏦 Contact your bank to report the unauthorized transaction
2. 🔒 Change your password on our website
3. 📧 Reply with details (amount, date) so I can escalate to our security team

We'll investigate this thoroughly. Your account security is our priority."""
        
        elif specialist == "ESCALATION":
            return f"""I sincerely apologize for your experience. As a senior manager, I'm personally taking ownership of this issue.

🔴 **Priority Escalation Initiated**

I'm escalating your case to our executive team right now. To ensure swift resolution:

1. Provide your preferred contact (phone/email)
2. Brief description of the issue
3. Any order/reference numbers

You'll receive a response within **24 hours**. I'll personally monitor this."""
        
        else:
            # General support
            return """👋 Hello! I'm here to help you today.

I can assist with:
• 📦 Order tracking and status
• 🔄 Returns and refunds
• 📊 Product availability
• 🔒 Security concerns
• ⬆️ Urgent issues

What can I help you with?"""

def get_status_message(status: str) -> str:
    """Return a friendly message based on order status.
    The status stored in the DB is uppercase (e.g., "SHIPPED").
    This function normalizes the input to uppercase and maps it to a user-friendly message.
    """
    status_upper = status.upper()
    status_messages = {
        "SHIPPED": "🚚 Your order is on the way!",
        "DELIVERED": "✅ Your order has been delivered.",
        "PROCESSING": "⏳ We're preparing your order for shipment.",
        "PENDING": "📝 Your order is being processed.",
        "CANCELLED": "❌ This order has been cancelled.",
    }
    return status_messages.get(status_upper, "")
