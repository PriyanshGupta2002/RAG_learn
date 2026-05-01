
from sentence_transformers import SentenceTransformer
_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Load the model
def create_embeddings(document_chunks):
    # Generate embeddings for the document chunks
    embeddings = _model.encode(document_chunks)
    return embeddings

