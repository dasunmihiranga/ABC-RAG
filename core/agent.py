# core/agent.py
# Contains the main Agent (ABCBot) logic 

from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda, RunnableBranch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from operator import itemgetter

from core.llm_setup import get_llm
from core.vector_store import get_vector_store, get_retriever
from core.prompt_templates import human_prompt

store = {}

# Define the out-of-knowledge response as per your prompt templates
OUT_OF_KNOWLEDGE_RESPONSE = "I apologize, but I don't have that specific information in my knowledge base at the moment. However, I can connect you directly with a human expert from our team who can assist you further. Would you like their contact details or for them to reach out to you?"

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_agent_chain():
    """
    Initializes and returns the main ABC Assistant agent chain.
    """
    llm = get_llm()
    vector_store = get_vector_store()
    retriever = get_retriever(vector_store)

    # Define the condition for the RunnableBranch
    def is_context_empty(input_dict):
        context = input_dict.get("context")
        return not context or all(not doc.page_content.strip() for doc in context)

    # Define the branch for when context is empty
    out_of_knowledge_branch = RunnableLambda(lambda x: OUT_OF_KNOWLEDGE_RESPONSE)

    # Define the main RAG processing branch
    rag_processing_branch = (
        human_prompt
        | llm
        | StrOutputParser()
    )

    # Define the full RAG chain with conditional logic
    full_rag_chain = (
        {
            "context": itemgetter("input") | retriever,
            "chat_history": itemgetter("chat_history"),
            "input": itemgetter("input"),
        }
        | RunnableBranch(
            (is_context_empty, out_of_knowledge_branch), # If context is empty, take this path
            rag_processing_branch, # Otherwise, take the RAG processing path
        )
    )

    # Wrap the RAG chain with message history
    with_message_history = RunnableWithMessageHistory(
        full_rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return with_message_history 