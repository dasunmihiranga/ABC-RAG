# core/vector_store.py
# Manages ChromaDB initialization and RAG retrieval 
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.embeddings import get_embedding_model
import os

CHROMA_DB_PATH = "./chroma_db"

def get_vector_store():
    """
    Initializes and returns the ChromaDB vector store.
    If the database does not exist, it will be created.
    """
    embeddings = get_embedding_model()
    
    # Ensure the ChromaDB directory exists
    if not os.path.exists(CHROMA_DB_PATH):
        os.makedirs(CHROMA_DB_PATH)

    vector_store = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return vector_store

def get_retriever(vector_store, k=4):
    """
    Returns a retriever for the given vector store.
    """
    return vector_store.as_retriever(search_kwargs={"k": k})

def split_documents(documents):
    """
    Splits documents into smaller chunks for ingestion into the vector store.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents) 