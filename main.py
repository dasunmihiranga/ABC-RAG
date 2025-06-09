# main.py
# This is the FastAPI application entry point, defines /chat API 
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from core.agent import get_agent_chain
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(
    title="Agentic RAG Chatbot API",
    description="API for Aura, a professional company assistant powered by Agentic RAG.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent chain
agent_chain = get_agent_chain()

class ChatRequest(BaseModel):
    query: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    try:
        response_raw = agent_chain.invoke(
            {"input": request.query},
            config={
                "configurable": {"session_id": request.session_id}
            },
        )

        # Ensure the response content is a string explicitly
        if isinstance(response_raw, AIMessage):
            response_content = str(response_raw.content)
        else:
            # For any other type, directly convert to string
            response_content = str(response_raw)
            
        return {"response": response_content}
    except Exception as e:
        # Log the full exception for debugging
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"} 