# Agentic RAG Chatbot

This project implements an Agentic RAG (Retrieval Augmented Generation) Chatbot, initially accessible via a web interface. The bot's primary role is to serve as a genuine and professional company assistant, capable of engaging with clients, understanding their needs, and effectively guiding them towards purchasing our services and products.

## Project Structure

```
assistant_agent/
├── venv/
├── .env
├── main.py
├── requirements.txt
├── README.md
├── core/
│   ├── __init__.py
│   ├── agent.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── llm_setup.py
│   └── prompt_templates.py
├── knowledge_base/
│   ├── __init__.py
│   └── docs/
│       ├── abc_company_info.md
└── scripts/
    ├── __init__.py
    └── ingest_data.py
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd assistant_agent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    Create a `.env` file in the `assistant_agent/` directory and add your API keys:
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    # Add any other necessary API keys here
    ```

## Running the Application

1.  **Ingest Knowledge Base Documents:**
    ```bash
    python scripts/ingest_data.py
    ```

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

*   **`/chat` (POST):** Accepts user queries and returns bot responses.
    *   **Request Body:**
        ```json
        {
            "query": "Your user query here",
            "session_id": "user1"
        }
        ```
    *   **Response Body:**
        ```json
        {
            "response": "Bot's reply here"
        }
        ``` 
