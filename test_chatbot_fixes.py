#!/usr/bin/env python3
"""
Test script to verify the chatbot fixes for:
1. Product matching (mouse vs keyboard)
2. Customer lookup (phone number queries)
"""

import requests
import json

CHATBOT_URL = "http://localhost:8005/api/chatbot/chat"

def test_chatbot(message: str, user_email: str = "test@example.com"):
    """Send a message to the chatbot and print the response"""
    print(f"\n{'='*60}")
    print(f"USER: {message}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            CHATBOT_URL,
            json={"message": message, "user_email": user_email},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"BOT: {data.get('response', 'No response')}")
            return data
        else:
            print(f"ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    print("\n🧪 Testing Chatbot Fixes")
    print("="*60)
    
    # Test 1: Mouse query should return mouse products, not keyboards
    print("\n📝 TEST 1: Product matching for 'mouse'")
    test_chatbot("I'm looking for a mouse")
    
    # Test 2: Monitor query should return monitors
    print("\n📝 TEST 2: Product matching for 'monitor'")  
    test_chatbot("Show me wireless monitor")
    
    # Test 3: Customer phone number lookup
    print("\n📝 TEST 3: Customer phone number lookup")
    test_chatbot("What's Bob Smith's phone number?")
    
    print("\n✅ Tests completed!")
