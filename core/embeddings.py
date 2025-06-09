# core/embeddings.py
# Initializes and provides the Hugging Face Embedding Model 

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Initializes and returns a Hugging Face Sentence Transformer embedding model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}  # Use 'cuda' if you have a GPU
    encode_kwargs = {'normalize_embeddings': False} # changed to false (default was True)
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf 