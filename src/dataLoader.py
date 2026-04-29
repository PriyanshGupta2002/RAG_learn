from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader,TextLoader,Docx2txtLoader,UnstructuredExcelLoader,JSONLoader
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader



def load_documents_from_urls(urls: List[str] = None) -> List[dict]:
    documents = []
    for url in urls:
        try:
            loader = UnstructuredURLLoader(urls=[url])
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"Loaded {len(loaded_docs)} documents from {url}")
        except Exception as e:
            print(f"Error loading {url}: {e}")
    return documents

def load_documents_from_directory(directory_path: str) -> List[dict]:
    """
    Load documents from a specified directory and return them as a list of dictionaries.
    
    Args:
        directory_path (str): The path to the directory containing the documents.
        Supports PDF, TXT, DOCX, EXCEL, and HTML files (searches subdirectories recursively)
    Returns:
        List[dict]: A list of dictionaries, each containing the content and metadata of a document.
    """
    documents = []
    dir_path = Path(directory_path)
    print(f"Loading documents from directory: {dir_path.absolute()}")

    # PDF files (recursive search in subdirectories)
    pdf_files = list(dir_path.glob("**/*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    for pdf_file in pdf_files:
        try:    
            loader = PyPDFLoader(str(pdf_file))
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source_file"] = str(pdf_file) 
                doc.metadata["file_type"] = "pdf"
                documents.append(doc)
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")

    # Text files (recursive search)
    txt_files = list(dir_path.glob("**/*.txt"))
    print(f"Found {len(txt_files)} TXT files")
    for txt_file in txt_files:
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source_file"] = str(txt_file)
                doc.metadata["file_type"] = "txt"
                documents.append(doc)
        except Exception as e:
            print(f"Error loading {txt_file}: {e}")

    # HTML files (recursive search)
    html_files = list(dir_path.glob("**/*.html"))
    print(f"Found {len(html_files)} HTML files")
    for html_file in html_files:
        try:
            from langchain_community.document_loaders import UnstructuredHTMLLoader
            loader = UnstructuredHTMLLoader(str(html_file))
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source_file"] = str(html_file)
                doc.metadata["file_type"] = "html"
                documents.append(doc)
        except Exception as e:
            print(f"Error loading {html_file}: {e}")

    # Excel files (recursive search)
    excel_files = list(dir_path.glob("**/*.xlsx")) + list(dir_path.glob("**/*.xls"))
    print(f"Found {len(excel_files)} Excel files")
    for excel_file in excel_files:
        try:
            loader = UnstructuredExcelLoader(str(excel_file), mode="elements")
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source_file"] = str(excel_file)
                doc.metadata["file_type"] = "excel"
                documents.append(doc)
        except Exception as e:
            print(f"Error loading {excel_file}: {e}")

    print(f"\n✓ Total documents loaded: {len(documents)}")
    return documents

def create_documents_chunks(documents: List[dict], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[dict]:
    """
    Create chunks from the loaded documents.
    
    Args:
        documents (List[dict]): A list of dictionaries containing document content and metadata.
        chunk_size (int): The size of each chunk in characters.
        chunk_overlap (int): The number of overlapping characters between chunks.
    
    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of content and its metadata.
    """
    

    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,length_function=len,
        separators=["\n\n", "\n", " ", ""])
    split_docs = text_splitter.split_documents(documents)
    if split_docs:
        print(f"Created {len(split_docs)} chunks from {len(documents)} documents.")
        print(f"Sample chunk content: {split_docs[0].page_content[:200]}...")  # Print the first 200 characters of the first chunk  
    return split_docs


    
