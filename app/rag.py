# app/rag.py
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables FIRST
load_dotenv()

def create_retriever():
    """
    Creates a retriever from the persistent Chroma vector store.
    """
    persist_directory = "./db"

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=OpenAIEmbeddings()
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever

def run_rag_query(question: str) -> str:
    """
    Takes a question, retrieves relevant documents, and returns them as a formatted string.
    """
    retriever = create_retriever()
    docs = retriever.invoke(question)
    
    context = "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    return f"Retrieved context:\n{context}"