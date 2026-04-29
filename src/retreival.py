from src.embeddings import create_embeddings
import chromadb
def retreiver(query,top_k,score_threshold=0.0):
    query_embeddings = create_embeddings([query])
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="documents",metadata={"hnsw:space": "cosine"})
    try:
        results =  collection.query(
            query_embeddings=query_embeddings,
            n_results=top_k
        )

        retreived_docs = []
        
        if results['documents'] and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            ids = results['ids'][0]
        
        for i,(doc,metadata,distance,id) in enumerate(zip(documents,metadatas,distances,ids)):
            similarity_score = 1 - distance  # Convert distance to similarity score (assuming cosine distance)
            if similarity_score >= score_threshold: 
                retreived_docs.append({
                    "id": id,
                    "content": doc,
                    "metadata": metadata,
                    "distance": distance,
                })
        return retreived_docs
    except Exception as e:
        print(f"Error occurred while retrieving documents: {e}")
        return []