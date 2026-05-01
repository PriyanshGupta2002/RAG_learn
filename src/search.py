from src.retrieval import retreiver
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import os

def search(query):
    top_k = 5
    score_threshold = 0.1
    retreived_docs = retreiver(query,top_k,score_threshold)
# Load environment variables

# Initialize the Groq model
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        raise ValueError("Groq API key not found. Please set the GROK_API_KEY environment variable.")

    llm = ChatGroq(
        api_key=grok_api_key,
        model="openai/gpt-oss-120b",
        temperature=0.1,
        max_tokens=1024,
    )

    print(f"✓ Groq LLM initialized with model: {llm.model_name} and temperature: {llm.temperature}")
    
    if not retreived_docs:
        return "No relevant documents found to answer the query. Please try a different question or load more data."
    
    context = "\n\n".join([f"Document {i+1}:\n{doc['content']}" for i, doc in enumerate(retreived_docs)])
    prompt = (
        "You are an assistant that provides answers based on the following retrieved documents:\n\n"
        f"{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )
    try:
        response = llm.invoke(prompt)
        # Handle different response types
        if hasattr(response, 'content'):
            answer = response.content.strip()
        else:
            answer = str(response).strip()
        
        # Fix escaped newlines in output
        answer = answer.replace('\\n', '\n')
        return answer
    except Exception as e:
        print(f"Error generating answer: {type(e).__name__}: {e}")
        return f"An error occurred while generating the answer."