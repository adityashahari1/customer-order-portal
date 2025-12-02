"""
Inventory management tools for checking and updating stock levels.
"""

from langchain_core.tools import tool
import requests
import os

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:8003")


@tool
def check_inventory(product_id: int) -> dict:
    """Check the inventory status for a given product ID.
    
    Args:
        product_id: The ID of the product to check
        
    Returns:
        Dict with quantity available and warehouse location
    """
    try:
        response = requests.get(f"{INVENTORY_SERVICE_URL}/{product_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Product not found"}
    except Exception as e:
        return {"error": str(e)}


@tool
def update_inventory(product_id: int, quantity_change: int) -> dict:
    """Update the inventory quantity for a product.
    
    Args:
        product_id: The ID of the product to update
        quantity_change: The change in quantity (positive or negative)
        
    Returns:
        Dict with updated inventory status
    """
    try:
        response = requests.post(
            f"{INVENTORY_SERVICE_URL}/update",
            json={"product_id": product_id, "quantity_change": quantity_change}
        )
        if response.status_code == 200:
            return response.json()
        else:
            # Attempt to return error from response if available, otherwise generic
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return {"error": f"Failed to update inventory: {response.text}"}
    except Exception as e:
        return {"error": str(e)}
