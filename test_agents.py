"""
Multi-Agent System Test Suite (Updated for LangChain)

Comprehensive tests for all 7 agents using the new LangChain framework.
"""

from datetime import datetime
from backend.agents.order_agent import process_new_order
from backend.agents.fraud_agent import analyze_transaction
from backend.agents.returns_agent import process_return
from backend.agents.inventory_intelligence_agent import analyze_inventory_levels
from backend.agents.salesforce_agent import sync_customer_data
from backend.agents.escalation_agent import escalate_issue
from backend.agents.orchestrator_agent import route_customer_query


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")


def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def test_orchestrator_agent():
    """Test Orchestrator Agent routing"""
    print_header("Testing Orchestrator Agent")
    
    try:
        result = route_customer_query(
            query="I need help with order #1001",
            customer_email="test@example.com"
        )
        
        if result.get('specialist'):
            print_success(f"Orchestrator Agent: Routed to {result['specialist']}")
            return True
        else:
            print_warning("Orchestrator returned no routing decision")
            return False
            
    except Exception as e:
        print_error(f"Orchestrator Agent failed: {str(e)}")
        return False


def test_order_agent():
    """Test Order Agent"""
    print_header("Testing Order Agent")
    
    order_data = {
        "order_id": 1001,
        "customer_id": "cus_test123",
        "items": [{"product_id": 1, "quantity": 2}],
        "total_amount": 100.0
    }
    
    try:
        result = process_new_order(order_data)
        
        if result.get('status'):
            print_success(f"Order Agent: {result['status']}")
            return True
        else:
            print_warning("Order Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Order Agent failed: {str(e)}")
        return False


def test_fraud_agent():
    """Test Fraud Agent"""
    print_header("Testing Fraud Agent")
    
    transaction_data = {
        "customer_id": "cus_suspicious",
        "transaction_amount": 5500.0,
        "transaction_count_24h": 15,
        "customer_email": "suspicious@example.com"
    }
    
    try:
        result = analyze_transaction(transaction_data)
        
        if result.get('status'):
            print_success(f"Fraud Agent: {result['status']}")
            return True
        else:
            print_warning("Fraud Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Fraud Agent failed: {str(e)}")
        return False


def test_returns_agent():
    """Test Returns Agent"""
    print_header("Testing Returns Agent")
    
    return_data = {
        "return_id": 2001,
        "order_id": 1001,
        "customer_id": "cus_test123",
        "items": [{"product_id": 1, "quantity": 1}],
        "reason": "Product defective",
        "charge_id": "ch_test123"
    }
    
    try:
        result = process_return(return_data)
        
        if result.get('status'):
            print_success(f"Returns Agent: {result['status']}")
            return True
        else:
            print_warning("Returns Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Returns Agent failed: {str(e)}")
        return False


def test_inventory_agent():
    """Test Inventory Intelligence Agent"""
    print_header("Testing Inventory Intelligence Agent")
    
    try:
        result = analyze_inventory_levels(product_id=1, threshold=10)
        
        if result.get('status'):
            print_success(f"Inventory Agent: {result['status']}")
            return True
        else:
            print_warning("Inventory Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Inventory Agent failed: {str(e)}")
        return False


def test_salesforce_agent():
    """Test Salesforce Agent"""
    print_header("Testing Salesforce Agent")
    
    customer_data = {
        "customer_email": "john.doe@example.com",
        "customer_name": "John Doe"
    }
    
    try:
        result = sync_customer_data(customer_data)
        
        if result.get('status'):
            print_success(f"Salesforce Agent: {result['status']}")
            return True
        else:
            print_warning("Salesforce Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Salesforce Agent failed: {str(e)}")
        return False


def test_escalation_agent():
    """Test Escalation Agent"""
    print_header("Testing Escalation Agent")
    
    escalation_data = {
        "customer_email": "angry@example.com",
        "issue_description": "Order never arrived after 2 weeks",
        "severity": "High"
    }
    
    try:
        result = escalate_issue(escalation_data)
        
        if result.get('status'):
            print_success(f"Escalation Agent: {result['status']}")
            return True
        else:
            print_warning("Escalation Agent returned unexpected format")
            return False
            
    except Exception as e:
        print_error(f"Escalation Agent failed: {str(e)}")
        return False


def test_agent_collaboration():
    """Test multi-agent collaboration via Orchestrator"""
    print_header("Testing Agent Collaboration")
    
    try:
        # Test routing to different specialists
        test_cases = [
            ("I need to return my order", "RETURNS"),
            ("This transaction looks suspicious", "FRAUD"),
            ("Check stock for product 123", "INVENTORY")
        ]
        
        all_passed = True
        for query, expected_specialist in test_cases:
            result = route_customer_query(query, "test@example.com")
            if expected_specialist in result.get('specialist', ''):
                print_success(f"Routed '{query[:30]}...' → {result['specialist']}")
            else:
                print_warning(f"Unexpected routing for '{query[:30]}...'")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_error(f"Collaboration test failed: {str(e)}")
        return False


def main():
    """Run all agent tests"""
    print_header("Multi-Agent System Test Suite (LangChain)")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info("LLM: Ollama (llama3.2:1b)")
    print_info("Framework: LangChain with direct tool calling")
    
    results = {
        "Orchestrator Agent": test_orchestrator_agent(),
        "Order Agent": test_order_agent(),
        "Fraud Agent": test_fraud_agent(),
        "Returns Agent": test_returns_agent(),
        "Inventory Intelligence Agent": test_inventory_agent(),
        "Salesforce Agent": test_salesforce_agent(),
        "Escalation Agent": test_escalation_agent(),
        "Agent Collaboration": test_agent_collaboration(),
    }
    
    # Summary
    print_header("Test Results Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for agent, result in results.items():
        if result:
            print_success(f"{agent}: PASSED")
        else:
            print_error(f"{agent}: FAILED")
    
    print(f"\n{Colors.BOLD}Overall: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print_success("🎉 All agent tests passed!")
    elif passed >= 6:
        print_warning(f"⚠️  {total - passed} agent(s) need attention")
    else:
        print_error(f"❌ {total - passed} agents failed - review needed")
    
    print_info(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n{Colors.OKCYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Note: Some agents may show warnings due to microservices not running.{Colors.ENDC}")
    print(f"{Colors.OKCYAN}This is expected behavior for isolated agent testing.{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*70}{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
