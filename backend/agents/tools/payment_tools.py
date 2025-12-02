"""
Payment processing tools using Stripe integration.
"""

from langchain_core.tools import tool
import stripe
import os

stripe.api_key = os.getenv("STRIPE_API_KEY")


@tool
def process_payment(amount: float, customer_id: str) -> dict:
    """Process a payment using Stripe.
    
    Args:
        amount: The amount to charge in dollars
        customer_id: The customer's Stripe ID
        
    Returns:
        Dict with status and charge_id if successful, or error message
    """
    try:
        charge = stripe.Charge.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            customer=customer_id,
            description="Order payment"
        )
        return {"status": "success", "charge_id": charge.id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@tool
def refund_payment(charge_id: str) -> dict:
    """Process a refund for a previous charge.
    
    Args:
        charge_id: The Stripe charge ID to refund
        
    Returns:
        Dict with status and refund_id if successful, or error message
    """
    try:
        refund = stripe.Refund.create(charge=charge_id)
        return {"status": "success", "refund_id": refund.id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
