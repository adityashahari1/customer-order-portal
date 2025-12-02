"""
Inventory Intelligence Agent

Monitors stock levels and recommends reorder quantities.
"""

from backend.agents.agent_framework import BaseAgent
from backend.agents.tools.inventory_tools import check_inventory, update_inventory


def analyze_inventory_levels(product_id: int, threshold: int = 10) -> dict:
    """
    Analyze inventory levels and recommend reorders.
    
    Args:
        product_id: The product ID to analyze
        threshold: Minimum stock level before reordering (default: 10)
        
    Returns:
        Dict with inventory analysis and recommendations
    """
    # Create Inventory Intelligence Agent
    agent = BaseAgent(
        role='Inventory Intelligence Analyst',
        goal='Monitor stock levels and optimize inventory',
        backstory="""You are an expert in inventory management and demand forecasting.
        You analyze stock levels and make data-driven reorder recommendations.""",
        tools=[check_inventory, update_inventory],
        verbose=True,
        max_iterations=3
    )
    
    task = f"""
    Analyze inventory for product {product_id} with reorder threshold of {threshold} units.
    
    Steps:
    1. Use check_inventory tool to get current stock level for product_id={product_id}
    2. If stock level is below {threshold}, calculate recommended reorder quantity (suggest 2x threshold)
    3. Return analysis with current stock, threshold, and reorder recommendation
    
    Final Answer should include:
    - Current stock level
    - Whether reorder is needed
    - Recommended reorder quantity (if needed)
    """
    
    result = agent.execute(task, context={"product_id": product_id, "threshold": threshold})
    
    # Parse result for reorder recommendation
    needs_reorder = "reorder" in result.lower() and ("needed" in result.lower() or "recommend" in result.lower())
    
    return {
        "product_id": product_id,
        "threshold": threshold,
        "needs_reorder": needs_reorder,
        "analysis": result,
        "status": "REORDER_RECOMMENDED" if needs_reorder else "STOCK_ADEQUATE"
    }
