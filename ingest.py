# ingest.py
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables (for OpenAI API key)
load_dotenv()

# --- 1. LOAD ---
logging.info("Loading documents...")
# Use a DirectoryLoader to load all .txt files from the 'data' folder
loader = DirectoryLoader("data/", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()
logging.info(f"Loaded {len(documents)} document(s).")

# --- 2. SPLIT ---
logging.info("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)
logging.info(f"Split into {len(splits)} chunks.")

# --- 3. EMBED & 4. STORE ---
logging.info("Creating vector store and embedding documents...")
# This one command does both the embedding and storing
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="./db" # This is the folder where the database will be saved
)
logging.info("Vector store created successfully in the 'db' folder.")