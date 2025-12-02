# 🚀 Quick Start: Testing Your AI Agents

## ✅ Your System is Ready!

All 7 agents have been successfully migrated and tested:
- ✅ Order Agent
- ✅ Fraud Detection Agent
- ✅ Returns Agent
- ✅ Inventory Intelligence Agent
- ✅ Salesforce Agent
- ✅ Escalation Agent
- ✅ Orchestrator Agent (Query Routing)

---

## 🎯 Three Simple Ways to Test

### **Method 1: Full Test Suite** (Recommended for validation)

```powershell
cd c:\Users\User\Desktop\ESP\customer-order-portal
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_all_agents.py
```

**Output:** Complete test of all 7 agents (~2-5 minutes)

---

### **Method 2: Quick Individual Agent Tests**

```powershell
# Test the Orchestrator (routing agent)
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_single_agent.py orchestrator

# Test the Order Agent
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_single_agent.py order

# Test the Fraud Detection Agent
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_single_agent.py fraud
```

**Output:** Quick focused tests for specific agents

---

### **Method 3: Interactive Python Testing**

```powershell
# Start Python with venv
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe

# Then in Python:
>>> from backend.agents.orchestrator_agent import route_customer_query
>>> route_customer_query("I want to return my order", "customer@example.com")
>>> 
>>> from backend.agents.fraud_agent import analyze_transaction
>>> analyze_transaction({
...     "customer_id": "test123",
...     "transaction_amount": 5000.0,
...     "transaction_count_24h": 20,
...     "customer_email": "test@example.com"
... })
```

---

## ⚙️ Advanced: Using Different Models

### Switch to the More Accurate Model

```powershell
# Set environment variable to use llama3.1:8b (more accurate)
$env:OLLAMA_MODEL_NAME = "llama3.1:8b"

# Then run tests
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_all_agents.py
```

**Model Comparison:**
- **llama3.2:1b** ⚡ (Current default): Fast, lightweight, good for development
- **llama3.1:8b** 🎯 (Available): More accurate, better reasoning, use for production

---

## 📊 What You'll See

When running tests, you'll see:

```
======================================================================
  1. Testing Order Agent
======================================================================

--- Iteration 1 ---
Response: [Tool calls]
Tool Call: check_inventory({'product_id': 1})
Tool Result: {'product_id': 1, 'available': 50, 'status': 'IN_STOCK'}

--- Iteration 2 ---
Tool Call: process_payment({'amount': 50.0, 'customer_id': 'cus_test123'})
Tool Result: {'status': 'success', 'charge_id': 'ch_...'}

[OK] Order Agent Test:
  Status: ORDER_PLACED
  Message: Successfully created order...
```

---

## 🔧 Troubleshooting

### Problem: "Model not found"
**Solution:**
```powershell
ollama pull llama3.2:1b
```

### Problem: "Connection refused"
**Solution:** Ensure Ollama is running:
```powershell
ollama list  # Should show available models
```

### Problem: Agent not performing well
**Solution:** Switch to larger model:
```powershell
$env:OLLAMA_MODEL_NAME = "llama3.1:8b"
```

---

## 📚 Full Documentation

For detailed information, see:
- **[AGENT_TESTING_GUIDE.md](file:///c:/Users/User/Desktop/ESP/customer-order-portal/AGENT_TESTING_GUIDE.md)** - Complete testing guide
- **[test_all_agents.py](file:///c:/Users/User/Desktop/ESP/customer-order-portal/test_all_agents.py)** - Full test suite
- **[test_single_agent.py](file:///c:/Users/User/Desktop/ESP/customer-order-portal/test_single_agent.py)** - Individual agent testing

---

## 🎉 You're All Set!

Your multi-agent AI system is now running on **100% open-source** models via Ollama, with no dependency on OpenAI or external APIs.

**Ready to test?** Run this now:

```powershell
cd c:\Users\User\Desktop\ESP\customer-order-portal
c:\Users\User\Desktop\ESP\.venv\Scripts\python.exe test_all_agents.py
```
