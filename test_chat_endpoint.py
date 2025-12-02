import requests
import json
import sys

# Set UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Test chatbot endpoint through gateway
url = "http://localhost:8000/api/chatbot/chat"
data = {
    "message": "I need help with my order",
    "user_email": "test@example.com"
}

print("Testing chatbot endpoint...")
print(f"URL: {url}")
print(f"Request: {json.dumps(data, indent=2)}")
print("-" * 50)

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")  # Limit response length
    
    if response.ok:
        result = response.json()
        print("\n[OK] Chatbot is working!")
        print(f"AI Response: {result.get('response', 'No response')[:200]}")
    else:
        print(f"\n[ERROR] Status Code: {response.status_code}")
        print(f"Details: {response.text[:500]}")
except requests.exceptions.ConnectionError as e:
    print(f"\n[ERROR] Connection Error: Cannot connect to {url}")
    print("Make sure the backend services are running")
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
