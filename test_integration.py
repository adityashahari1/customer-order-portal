"""
Frontend-Backend Integration Test

This script tests the AI chatbot integration between frontend and backend.
"""

import requests
import json
import time

API_URL = "http://localhost:8000/api/chatbot/chat"
FRONTEND_URL = "http://localhost:5173"

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def test_health_check():
    """Test if the chatbot service is healthy"""
    print_header("1. Testing Backend Health")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend is healthy:", response.json())
            return True
        else:
            print("[FAIL] Backend health check failed")
            return False
    except Exception as e:
        print(f"[FAIL] Cannot connect to backend: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print_header("2. Testing Frontend")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"[OK] Frontend is accessible at {FRONTEND_URL}")
            return True
        else:
            print("[FAIL] Frontend returned non-200 status")
            return False
    except Exception as e:
        print(f"[FAIL] Cannot connect to frontend: {e}")
        return False

def test_chat_message(message, user_email="test@example.com"):
    """Send a message to the chatbot and get a response"""
    print(f"\nUser: {message}")
    
    payload = {
        "message": message,
        "user_email": user_email
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # AI can take time to respond
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "No response")
            print(f"AI ({elapsed:.1f}s): {ai_response[:200]}{'...' if len(ai_response) > 200 else ''}")
            return True, ai_response
        else:
            print(f"[FAIL] API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"[FAIL] Error calling chat API: {e}")
        return False, None

def main():
    print("\n" + "#" * 70)
    print("#  Customer Order Portal - AI Agent Integration Test")
    print("#  Testing frontend-backend-agent communication")
    print("#" * 70)
    
    # Test 1: Backend Health
    backend_ok = test_health_check()
    
    # Test 2: Frontend Accessibility
    frontend_ok = test_frontend()
    
    if not backend_ok:
        print("\n[ERROR] Backend is not running. Start it with:")
        print("  cd c:\\Users\\User\\Desktop\\ESP\\customer-order-portal")
        print("  c:\\Users\\User\\Desktop\\ESP\\.venv\\Scripts\\python.exe -m uvicorn backend.services.chatbot_service.main:app --port 8000")
        return
    
    if not frontend_ok:
        print("\n[WARNING] Frontend may not be running. Start it with:")
        print("  cd c:\\Users\\User\\Desktop\\ESP\\customer-order-portal\\frontend")
        print("  npm run dev")
    
    # Test 3: Chat Interactions
    print_header("3. Testing AI Chat Interactions")
    
    test_cases = [
        {
            "name": "Returns Request",
            "message": "I need to return my laptop because it's defective",
            "expected_keywords": ["return", "refund", "RETURNS"]
        },
        {
            "name": "Order Status",
            "message": "Where is my order #12345?",
            "expected_keywords": ["order", "status", "ORDER"]
        },
        {
            "name": "Fraud Alert",
            "message": "I see suspicious charges on my account",
            "expected_keywords": ["fraud", "security", "FRAUD"]
        },
        {
            "name": "Escalation",
            "message": "This is terrible! I want to speak to a manager!",
            "expected_keywords": ["escalation", "manager", "ESCALATION"]
        },
        {
            "name": "Inventory Check",
            "message": "Do you have MacBook Pro in stock?",
            "expected_keywords": ["inventory", "stock", "INVENTORY"]
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n--- Test: {test_case['name']} ---")
        success, response = test_chat_message(test_case['message'])
        
        if success and response:
            # Check if expected keywords are in response
            response_upper = response.upper()
            found_keywords = [kw for kw in test_case['expected_keywords'] if kw.upper() in response_upper]
            
            if found_keywords:
                print(f"  [OK] Found expected keywords: {found_keywords}")
                results[test_case['name']] = "PASS"
            else:
                print(f"  [WARNING] Expected keywords not found: {test_case['expected_keywords']}")
                results[test_case['name']] = "PARTIAL"
        else:
            results[test_case['name']] = "FAIL"
        
        # Wait between tests to avoid overwhelming the AI
        time.sleep(2)
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v == "PASS")
    partial = sum(1 for v in results.values() if v == "PARTIAL")
    failed = sum(1 for v in results.values() if v == "FAIL")
    total = len(results)
    
    for test_name, result in results.items():
        status_icon = "[PASS]" if result == "PASS" else "[WARN]" if result == "PARTIAL" else "[FAIL]"
        print(f"  {status_icon}: {test_name}")
    
    print(f"\n  Overall: {passed} passed, {partial} partial, {failed} failed out of {total}")
    
    if passed + partial == total:
        print("\n  SUCCESS: All agents are responding!")
        print("\n  Your portal is ready for demo! Open:")
        print(f"    {FRONTEND_URL}")
        print("\n  Click the chat button in the bottom-right corner to interact with AI agents.")
    else:
        print("\n  ATTENTION: Some tests failed. Check the logs above.")
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
