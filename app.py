from src.dataLoader import load_documents_from_directory, create_documents_chunks, load_documents_from_urls
from src.embeddings import create_embeddings
from src.vectorStore import create_vector_store
from src.search import search
import chromadb

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="documents",metadata={"hnsw:space": "cosine"})

    print("=" * 80)
    print("RAG PIPELINE STARTED")
    print("=" * 80)
    
    # Sources to load from
    urls = [
        "https://www.prisma.io/docs/prisma-postgres/import-from-existing-database-postgresql",
        "https://www.prisma.io/docs/prisma-postgres/import-from-existing-database-mysql",
        "https://www.prisma.io/docs/orm/core-concepts/data-modeling",
        "https://react.dev/reference/react/hooks"
    ]
    
    documents = []
    if collection.count() == 0:
    # Step 1a: Load from URLs
        print("\n[Step 1a] Loading documents from URLs...")
        try:
            url_documents = load_documents_from_urls(urls=urls)
            documents.extend(url_documents)
            print(f"✓ Loaded {len(url_documents)} documents from URLs")
        except Exception as e:
            print(f"✗ Error loading from URLs: {e}")
        
        # Step 1b: Load from local directory
        # print("\n[Step 1b] Loading documents from local directory...")
        # try:
        #     local_documents = load_documents_from_directory("data")
        #     documents.extend(local_documents)
        #     print(f"✓ Loaded {len(local_documents)} documents from local directory")
        # except Exception as e:
        #     print(f"✗ Error loading from local directory: {e}")
        
        # Check if we have any documents
        if not documents:
            print("\n✗ No documents loaded from any source!")
            exit(1)
        
        print(f"\n✓ Total documents loaded: {len(documents)} (from both sources combined)")
        
        # Step 2: Create chunks
        print("\n[Step 2] Creating document chunks...")
        document_chunks = create_documents_chunks(documents, chunk_size=1000, chunk_overlap=200)
        print(f"✓ Created {len(document_chunks)} chunks from {len(documents)} documents")
        
        # Step 3: Generate embeddings
        print("\n[Step 3] Generating embeddings...")
        texts = [chunk.page_content for chunk in document_chunks]
        print(f"  Processing {len(texts)} text chunks...")
        embeddings = create_embeddings(texts)
        print(f"✓ Generated embeddings for {len(document_chunks)} document chunks")
        
        # Step 4: Create vector store
        print("\n[Step 4] Creating vector store...")
        create_vector_store(embeddings, document_chunks)
        print(f"✓ Vector store created and populated")
        
    # Step 5: Search and generate answer
    print("\n[Step 5] Searching and generating answer...")
    query = "What is use of useEffect hook in React?"
    print(f"  Query: {query}")
    answer = search(query)
    
    print("\n" + "=" * 80)
    print("ANSWER:")
    print("=" * 80)
    print(answer)
    print("=" * 80)