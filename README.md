# Customer Order Management Portal

A production-ready microservices system with multi-agent AI orchestration.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop (for PostgreSQL, Redis, RabbitMQ)
- Ollama (for local AI models)

## Setup

1.  **Initialize Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```

2.  **Install Backend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Frontend Dependencies**:
    ```bash
    cd frontend
    npm install
    ```

4.  **Setup AI Models**:
    Ensure Ollama is installed and running, then pull the required model:
    ```bash
    ollama pull llama3.2:1b
    ```

5.  **Start Infrastructure**:
    Ensure Docker Desktop is running, then:
    ```bash
    cd infrastructure
    docker-compose up -d
    ```

## Running the Application

1.  **Start Microservices**:
    In the root directory:
    ```bash
    python run_services.py
    ```
    This starts all 8 microservices + API Gateway.

2.  **Start Frontend**:
    In a new terminal:
    ```bash
    cd frontend
    npm run dev
    ```

3.  **Access the Portal**:
    Open [http://localhost:5173](http://localhost:5173) in your browser.

## Architecture

- **Backend**: FastAPI Microservices (Ports 8001-8008)
- **Gateway**: FastAPI (Port 8000)
- **Frontend**: React + TypeScript + Vite
- **AI**: LangChain + Ollama (Local LLMs)
- **Database**: PostgreSQL
- **Messaging**: RabbitMQ
- **Caching**: Redis

## API Documentation

Access Swagger UI for individual services:
- Order Service: [http://localhost:8001/docs](http://localhost:8001/docs)
- Inventory Service: [http://localhost:8003/docs](http://localhost:8003/docs)
- ...and so on.
