from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

# Folder where your PDFs live
DATA_FOLDER = "./data"
CHROMA_PATH = "./chroma_store"

_embeddings = None

def get_embeddings():
    """Lazy load embedding model so startup is not blocked."""
    global _embeddings
    if _embeddings is None:
        print("[RAG] Initializing SentenceTransformerEmbeddings (all-MiniLM-L6-v2)...")
        _embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings

def ingest_documents(max_pages=80):
    """Load PDFs from data/ folder, chunk them, embed and store in ChromaDB."""
    all_docs = []

    if not os.path.exists(DATA_FOLDER):
        print("Data folder does not exist!")
        return None

    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDFs found in data/ folder!")
        return None

    print(f"Found {len(pdf_files)} PDF(s): {pdf_files}")

    for filename in pdf_files:
        path = os.path.join(DATA_FOLDER, filename)
        print(f"Loading {filename} (indexing up to {max_pages} key pages)...")
        loader = PyPDFLoader(path)
        docs = loader.load()
        if max_pages and len(docs) > max_pages:
            docs = docs[:max_pages]
        all_docs.extend(docs)
        print(f"  → {len(docs)} pages loaded")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks created: {len(chunks)}")

    # Store in ChromaDB
    print("Embedding and storing in ChromaDB...")
    vectorstore = Chroma.from_documents(
        chunks,
        get_embeddings(),
        persist_directory=CHROMA_PATH,
    )
    print(f"Done! {len(chunks)} chunks stored in ChromaDB.")
    return vectorstore

def get_retriever():
    """Load existing ChromaDB and return a retriever. Ingests key pages if not present."""
    if not os.path.exists(CHROMA_PATH) or not os.listdir(CHROMA_PATH):
        print("[RAG] ChromaDB vector store not found or empty. Running initial ingestion...")
        ingest_documents(max_pages=80)

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings(),
    )
    return vectorstore.as_retriever(search_kwargs={"k": 4})