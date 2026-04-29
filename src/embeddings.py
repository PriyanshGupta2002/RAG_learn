
from sentence_transformers import SentenceTransformer

# Load the model
def create_embeddings(document_chunks):
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    # Generate embeddings for the document chunks
    embeddings = model.encode(document_chunks)
    return embeddings

