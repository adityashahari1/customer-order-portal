"""
Multi-Agent System Demonstration
This script demonstrates the multi-agent architecture and workflow without external dependencies.
"""
import asyncio
from datetime import datetime

# Color output for better readability
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}[SUCCESS] {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}[INFO] {text}{Colors.ENDC}")

def print_agent(agent_name, action):
    print(f"{Colors.OKCYAN}[{agent_name}] {action}{Colors.ENDC}")

def print_section(text):
    print(f"\n{Colors.BOLD}>>> {text}{Colors.ENDC}")

# Simulated Agent Classes
class Agent:
    def __init__(self, name, role, capabilities):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        print_success(f"{name} initialized - Role: {role}")

class OrchestratorAgent(Agent):
    def __init__(self):
        super().__init__(
            "Orchestrator Agent",
            "Customer Service Coordinator",
            ["task_delegation", "agent_coordination", "workflow_management"]
        )
    
    async def delegate_task(self, task):
        print_agent(self.name, f"Received task: '{task}'")
        await asyncio.sleep(0.5)
        
        # Determine which agent to delegate to
        if "order" in task.lower():
            return {"delegated_to": "Order Processing Agent", "task": task}
        elif "fraud" in task.lower():
            return {"delegated_to": "Fraud Detection Agent", "task": task}
        elif "return" in task.lower():
            return {"delegated_to": "Returns Agent", "task": task}
        else:
            return {"delegated_to": "Order Processing Agent", "task": task}

class OrderAgent(Agent):
    def __init__(self):
        super().__init__(
            "Order Processing Agent",
            "Order Fulfillment Specialist",
            ["validate_orders", "check_inventory", "process_payment"]
        )
    
    async def process_order(self, order_data):
        print_agent(self.name, f"Processing order for customer {order_data['customer_id']}")
        await asyncio.sleep(0.5)
        
        print_agent(self.name, "Step 1: Validating order...")
        await asyncio.sleep(0.3)
        print_agent(self.name, "Step 2: Checking inventory...")
        await asyncio.sleep(0.3)
        print_agent(self.name, "Step 3: Processing payment...")
        await asyncio.sleep(0.3)
        
        return {
            "status": "ORDER_CONFIRMED",
            "order_id": 1007,
            "total_amount": order_data['total'],
            "estimated_delivery": "3-5 business days"
        }

class FraudAgent(Agent):
    def __init__(self):
        super().__init__(
            "Fraud Detection Agent",
            "Security & Risk Analyst",
            ["analyze_patterns", "detect_anomalies", "risk_assessment"]
        )
    
    async def analyze_transaction(self, transaction_data):
        print_agent(self.name, f"Analyzing transaction for order #{transaction_data['order_id']}")
        await asyncio.sleep(0.5)
        
        # Simple rule-based fraud detection
        risk_level = "LOW"
        if transaction_data['amount'] > 10000:
            risk_level = "HIGH"
        elif transaction_data['amount'] > 1000:
            risk_level = "MEDIUM"
        
        print_agent(self.name, f"Risk assessment: {risk_level}")
        
        return {
            "risk_level": risk_level,
            "order_id": transaction_data['order_id'],
            "recommendation": "APPROVE" if risk_level != "HIGH" else "REVIEW"
        }

class ReturnsAgent(Agent):
    def __init__(self):
        super().__init__(
            "Returns Processing Agent",
            "Returns & Refunds Specialist",
            ["validate_returns", "process_refunds", "update_inventory"]
        )
    
    async def validate_return(self, return_data):
        print_agent(self.name, f"Validating return for order #{return_data['order_id']}")
        await asyncio.sleep(0.5)
        
        print_agent(self.name, f"Reason: {return_data['reason']}")
        print_agent(self.name, "Checking return policy...")
        await asyncio.sleep(0.3)
        
        return {
            "status": "RETURN_APPROVED",
            "refund_amount": 129.99,
            "return_id": "RET-1001"
        }

class InventoryAgent(Agent):
    def __init__(self):
        super().__init__(
            "Inventory Intelligence Agent",
            "Inventory Optimization Specialist",
            ["analyze_stock_levels", "predict_demand", "optimize_reorder"]
        )
    
    async def analyze_stock_levels(self):
        print_agent(self.name, "Analyzing current inventory levels...")
        await asyncio.sleep(0.5)
        
        return {
            "low_stock_items": 3,
            "out_of_stock_items": 1,
            "reorder_recommendations": ["27\" 4K Monitor", "Mechanical Keyboard"]
        }

class SalesforceAgent(Agent):
    def __init__(self):
        super().__init__(
            "Salesforce Sync Agent",
            "CRM Integration Specialist",
            ["sync_customer_data", "update_opportunities", "track_interactions"]
        )
    
    async def sync_customer_data(self, customer_data):
        print_agent(self.name, f"Syncing customer data for {customer_data['name']}")
        await asyncio.sleep(0.5)
        
        return {
            "status": "SYNCED",
            "salesforce_id": "SF-001",
            "customer_id": customer_data['customer_id']
        }

class EscalationAgent(Agent):
    def __init__(self):
        super().__init__(
            "Escalation Management Agent",
            "Critical Issue Handler",
            ["handle_escalations", "notify_supervisors", "emergency_response"]
        )
    
    async def handle_escalation(self, escalation_data):
        print_agent(self.name, f"Handling {escalation_data['priority']} priority escalation")
        await asyncio.sleep(0.5)
        
        print_agent(self.name, f"Issue: {escalation_data['issue']}")
        print_agent(self.name, "Notifying supervisor...")
        
        return {
            "status": "ESCALATED",
            "assigned_to": "Senior Support Manager",
            "ticket_id": escalation_data['ticket_id']
        }

async def demo_scenario_1():
    """Scenario 1: New Order Processing with Fraud Check"""
    print_section("SCENARIO 1: New Order Processing with Fraud Detection")
    
    orchestrator = OrchestratorAgent()
    order_agent = OrderAgent()
    fraud_agent = FraudAgent()
    
    print_info("Customer places a new order for $299.99")
    
    # Step 1: Orchestrator receives task
    delegation_result = await orchestrator.delegate_task("Process new order for customer #1")
    print_info(f"Task delegated to: {delegation_result['delegated_to']}")
    
    # Step 2: Fraud check
    fraud_result = await fraud_agent.analyze_transaction({
        "order_id": 1007,
        "amount": 299.99,
        "customer_id": 1
    })
    
    # Step 3: If approved, process order
    if fraud_result['recommendation'] == "APPROVE":
        order_result = await order_agent.process_order({
            "customer_id": 1,
            "items": [{"product_id": 8, "quantity": 1}],
            "total": 299.99
        })
        print_success(f"Order #{order_result['order_id']} confirmed! Delivery: {order_result['estimated_delivery']}")
    else:
        print_info("Order flagged for manual review")

async def demo_scenario_2():
    """Scenario 2: Return Processing"""
    print_section("SCENARIO 2: Customer Return Request")
    
    returns_agent = ReturnsAgent()
    inventory_agent = InventoryAgent()
    
    print_info("Customer requests return for defective headphones")
    
    # Process return
    return_result = await returns_agent.validate_return({
        "order_id": 1001,
        "reason": "Product defective",
        "customer_id": 1
    })
    
    print_success(f"Return approved! Refund: ${return_result['refund_amount']}")
    
    # Inventory checks stock after return
    inventory_result = await inventory_agent.analyze_stock_levels()
    print_info(f"Inventory update: {inventory_result['low_stock_items']} items need reordering")

async def demo_scenario_3():
    """Scenario 3: High-Value Order with Escalation"""
    print_section("SCENARIO 3: High-Value Order Requiring Escalation")
    
    fraud_agent = FraudAgent()
    escalation_agent = EscalationAgent()
    salesforce_agent = SalesforceAgent()
    
    print_info("Customer places a $15,000 order (suspicious)")
    
    # Fraud detection
    fraud_result = await fraud_agent.analyze_transaction({
        "order_id": 1008,
        "amount": 15000,
        "customer_id": 1
    })
    
    # If high risk, escalate
    if fraud_result['risk_level'] == "HIGH":
        escalation_result = await escalation_agent.handle_escalation({
            "ticket_id": 102,
            "priority": "HIGH",
            "issue": "Potential fraudulent transaction"
        })
        print_success(f"Escalated to: {escalation_result['assigned_to']}")
        
        # Sync to CRM for tracking
        await salesforce_agent.sync_customer_data({
            "customer_id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com"
        })
        print_success("Customer flagged in Salesforce CRM")

async def main():
    """Run all demonstration scenarios"""
    print_header("Multi-Agent System Architecture Demonstration")
    print_info(f"Demonstration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_info("\nThis demonstration shows 7 AI agents working together:")
    print_info("1. Orchestrator Agent - Coordinates all other agents")
    print_info("2. Order Processing Agent - Handles order fulfillment")
    print_info("3. Fraud Detection Agent - Analyzes transactions for risk")
    print_info("4. Returns Agent - Processes returns and refunds")
    print_info("5. Inventory Intelligence Agent - Optimizes stock levels")
    print_info("6. Salesforce Sync Agent - Integrates with CRM")
    print_info("7. Escalation Management Agent - Handles critical issues")
    
    # Run scenarios
    await demo_scenario_1()
    await asyncio.sleep(1)
    
    await demo_scenario_2()
    await asyncio.sleep(1)
    
    await demo_scenario_3()
    
    # Summary
    print_header("Demonstration Complete")
    print_success("All 7 agents are operational and working together!")
    print_info("The agents communicated seamlessly to handle:")
    print_info("  - Order processing with fraud detection")
    print_info("  - Return validation and inventory updates")
    print_info("  - High-risk transaction escalation to supervisors")
    print_info(f"\nDemonstration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print("1. Start Docker Desktop")
    print("2. Run: docker-compose up -d (in infrastructure folder)")
    print("3. Run: python run_services.py")
    print("4. Agents will connect to live backend services")

if __name__ == "__main__":
    asyncio.run(main())
