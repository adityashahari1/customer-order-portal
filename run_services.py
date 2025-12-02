import subprocess
import sys
import time
import os

services = [
    {"name": "API Gateway", "port": 8000, "path": "backend.services.gateway_service.main:app"},
    {"name": "Order Service", "port": 8001, "path": "backend.services.order_service.main:app"},
    {"name": "Returns Service", "port": 8002, "path": "backend.services.returns_service.main:app"},
    {"name": "Inventory Service", "port": 8003, "path": "backend.services.inventory_service.main:app"},
    {"name": "Customer Service", "port": 8004, "path": "backend.services.customer_service.main:app"},
    {"name": "Chatbot Service", "port": 8005, "path": "backend.services.chatbot_service.main:app"},
    {"name": "Salesforce Service", "port": 8006, "path": "backend.services.salesforce_service.main:app"},
    {"name": "Notification Service", "port": 8007, "path": "backend.services.notification_service.main:app"},
    {"name": "Analytics Service", "port": 8008, "path": "backend.services.analytics_service.main:app"},
]

processes = []

def start_services():
    print("Starting all microservices...")
    for service in services:
        print(f"Starting {service['name']} on port {service['port']}...")
        # Use sys.executable to ensure we use the same python interpreter (virtualenv)
        p = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", service['path'], "--host", "0.0.0.0", "--port", str(service['port'])],
            cwd=os.getcwd()
        )
        processes.append(p)
        time.sleep(1) # Give it a moment to start

    print("All services started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        for p in processes:
            p.terminate()
        print("Services stopped.")

if __name__ == "__main__":
    start_services()
