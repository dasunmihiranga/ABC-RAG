# scripts/ingest_data.py
# Script to process docs and load them into ChromaDB 

import os
import sys
# Add the parent directory to the system path to allow importing modules from 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from core.vector_store import get_vector_store, split_documents

DOCS_PATH = "./knowledge_base/docs"

def load_documents():
    """
    Loads documents from the knowledge_base/docs directory.
    """
    documents = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if os.path.isfile(filepath):
            if filename.endswith(".txt"):
                loader = TextLoader(filepath)
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(filepath) # using UnstructuredMarkdownLoader for .md files
            else:
                print(f"Skipping unsupported file: {filename}")
                continue
            documents.extend(loader.load())
    return documents

if __name__ == "__main__":
    print("Starting data ingestion...")
    vector_store = get_vector_store()
    
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    splits = split_documents(documents)
    print(f"Split into {len(splits)} chunks.")

    print("Adding document chunks to ChromaDB...")
    vector_store.add_documents(splits)
    # vector_store.persist() # Removed: No longer needed for ChromaDB 0.4.x and above
    print("Data ingestion complete.") 