

import chromadb
import uuid

_client = chromadb.PersistentClient(path="./chroma_db")
def getCollection():
    collection = _client.get_or_create_collection(name="documents",metadata={"hnsw:space": "cosine"})
    return collection

def create_vector_store(embeddings, document_chunks):
    collection = getCollection()
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} items. Skipping vector store creation.")
        return
    # Add document chunks and their corresponding embeddings to the collection
    embedding_list = []
    docTexts=[]
    ids=[]
    metaDatas=[]

    for i,(doc,embedding) in enumerate(zip(document_chunks,embeddings)):
        ids.append(str(uuid.uuid4()))  # Generate a unique ID for each document chunk
        docTexts.append(doc.page_content)
        metadata = dict(doc.metadata)  # Convert metadata to a regular dictionary
        metadata["source"] = doc.metadata.get("source_file", "unknown")  # Add source file info to metadata
        metadata['content_length'] = len(doc.page_content)  # Add content length to metadata
        metadata['authors'] = doc.metadata.get("authors", "unknown")  # Add authors info to metadata
        embedding_list.append(embedding.tolist())  # Convert numpy array to list for ChromaDB
        metaDatas.append(metadata)
    print(f"Prepared {len(document_chunks)} document chunks for vector store with metadata.")
    try:
        collection.add(
            ids=ids,
            documents=docTexts,
            metadatas=metaDatas,
            embeddings=embedding_list
        )

        print(f"Added {len(document_chunks)} document chunks to the vector store.") 
    except Exception as e:
        print(f"Error adding document chunks to the vector store: {e}")

