# RAG System Setup Guide

This guide will help you set up and run the RAG (Retrieval-Augmented Generation) system locally.

## 📋 Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/)
- **Groq API Key** - [Get Groq API Key](https://console.groq.com/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd RAG
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you're using `uv` (faster):
```bash
uv add -r requirements.txt
```

### 4. Setup Environment Variables

Copy the `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env` and add your credentials:
```
GROK_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

You should see output like:
```
================================================================================
RAG PIPELINE STARTED
================================================================================

[Step 1a] Loading documents from URLs...
✓ Loaded 45 documents from URLs

[Step 1b] Loading documents from local directory...
✓ Loaded 12 documents from local directory

✓ Total documents loaded: 57 (from both sources combined)

[Step 2] Creating document chunks...
✓ Created 145 chunks from 57 documents

[Step 3] Generating embeddings...
  Processing 145 text chunks...
✓ Generated embeddings for 145 document chunks

[Step 4] Creating vector store...
✓ Vector store created and populated

[Step 5] Searching and generating answer...
  Query: Give me an example on application level how would you write code for model in prisma?

================================================================================
ANSWER:
================================================================================
[LLM generated answer here...]
================================================================================
```

---

## 📁 Project Structure

```
RAG/
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── README.md             # Project documentation
├── SETUP.md              # This file
├── pyproject.toml        # Project metadata
├── .gitignore            # Git ignore rules
│
├── src/                  # Source code
│   ├── __init__.py
│   ├── dataLoader.py     # Document loading from URLs and directories
│   ├── embeddings.py     # Embedding generation
│   ├── vectorStore.py    # ChromaDB vector store management
│   ├── retreival.py      # Document retrieval
│   └── search.py         # Search and LLM integration
│
├── notebook/             # Jupyter notebooks (for experimentation)
│   ├── document.ipynb
│   └── pdf-loader.ipynb
│
└── data/                 # Data directory (not pushed to Git)
    ├── pdf_files/        # PDF documents
    ├── text_files/       # Text documents
    ├── html_files/       # HTML documents
    ├── excel_files/      # Excel files
    └── vector_store/     # ChromaDB storage (auto-generated)
```

---

## 🔧 Configuration

### Data Sources

The system loads documents from **two sources**:

#### 1. **Online URLs** (in `app.py`)
```python
urls = [
    "https://www.prisma.io/docs/prisma-postgres/import-from-existing-database-postgresql",
    "https://www.prisma.io/docs/prisma-postgres/import-from-existing-database-mysql",
    "https://www.prisma.io/docs/orm/core-concepts/data-modeling"
]
```

To add more URLs, edit these lines in `app.py`.

#### 2. **Local Files** (in `data/` directory)
- Place PDF, TXT, HTML, or Excel files in `data/` folder
- System automatically loads all files recursively

### Customize Your Query

Edit the query in `app.py`:
```python
query = "Your custom question here?"
```

### Adjust Search Parameters

In `src/search.py`:
```python
def search(query):
    top_k = 5                    # Number of documents to retrieve
    score_threshold = 0.1        # Minimum relevance score (0.0-1.0)
```

---

## 🛠️ Troubleshooting

### Issue: "Groq API key not found"
**Solution:** Make sure you have created `.env` file with `GROK_API_KEY` set.
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

### Issue: "Collection expecting embedding with dimension of 384, got 768"
**Solution:** Delete the old vector store and regenerate it:
```bash
Remove-Item -Recurse -Force "./chroma_db"  # Windows PowerShell
rm -rf ./chroma_db                         # macOS/Linux
```
Then run `python app.py` again.

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Issue: Very slow first run
**Solution:** This is normal! The system:
- Downloads and processes documents (first time only)
- Generates embeddings for all chunks
- Creates vector store

Subsequent runs are much faster (2-3 seconds).

---

## 📊 Performance Tips

1. **Reduce Data Size** - Start with fewer URLs/files
2. **Adjust Chunk Size** - In `dataLoader.py`:
   ```python
   create_documents_chunks(documents, chunk_size=500)  # Smaller chunks = faster
   ```
3. **Use Smaller Embedding Model** - Already using `all-MiniLM-L6-v2` (384 dims)

---

## 🔄 How It Works

```
User Query
    ↓
[1] Load Documents (URLs + Local Files)
    ↓
[2] Split into Chunks
    ↓
[3] Generate Embeddings
    ↓
[4] Store in Vector DB (ChromaDB)
    ↓
[5] Retrieve Similar Documents
    ↓
[6] Send to LLM (Groq)
    ↓
Generated Answer
```

---

## 🚀 Advanced Usage

### Using Jupyter Notebooks

For experimentation, use the provided notebooks:

```bash
jupyter notebook
```

Then open:
- `notebook/document.ipynb` - Data exploration
- `notebook/pdf-loader.ipynb` - RAG pipeline walkthrough

### Modifying LLM Model

In `src/search.py`, change the model:
```python
llm = ChatGroq(
    api_key=grok_api_key,
    model="mixtral-8x7b-32768",  # Options: llama-3-70b-8192, llama-3-8b-8192
    temperature=0.7,
    max_tokens=1024,
)
```

### Adding Custom Data

1. Place files in `data/` folder
2. Run `python app.py`
3. The system automatically detects and loads them

---

## 📝 Example Queries

Try these queries with the Prisma documentation:

```
"What is data modeling in Prisma?"
"How do I import from existing database?"
"Show me a code example for Prisma models"
"What are the differences between PostgreSQL and MySQL in Prisma?"
```

---

## 🐛 Debug Mode

Enable verbose logging (optional):

Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ❓ FAQ

**Q: Can I use a different LLM instead of Groq?**
A: Yes! Install `langchain-openai`, `langchain-anthropic`, etc. and modify `src/search.py`.

**Q: How much storage does ChromaDB use?**
A: Depends on document size. Generally 1MB of text = ~1MB in ChromaDB.

**Q: Can I use GPU for faster embeddings?**
A: Yes, install `torch` with CUDA support for GPU acceleration.

**Q: Is this suitable for production?**
A: For production, consider: adding authentication, implementing caching, using enterprise vector DB (Pinecone, Weaviate), and adding monitoring.

---

## 📞 Support

For issues:
1. Check this SETUP.md file
2. Review error messages carefully
3. Check `.env` file is correctly configured
4. Delete `chroma_db` folder and retry

---

## 📄 License

[Add your license here]

---

Happy RAG! 🎉
