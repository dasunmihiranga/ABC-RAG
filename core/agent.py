# core/agent.py
# Contains the main Agent (LeapBot) logic 

from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from operator import itemgetter

from core.llm_setup import get_llm
from core.vector_store import get_vector_store, get_retriever
from core.prompt_templates import human_prompt

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_agent_chain():
    """
    Initializes and returns the main Aura agent chain.
    """
    llm = get_llm()
    vector_store = get_vector_store()
    retriever = get_retriever(vector_store)

    # Define the RAG chain
    rag_chain = (
        {
            "context": itemgetter("input") | retriever,
            "chat_history": itemgetter("chat_history"),
            "input": itemgetter("input"),
        }
        | human_prompt
        | llm
        | StrOutputParser()
    )

    # Wrap the RAG chain with message history
    with_message_history = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return with_message_history 