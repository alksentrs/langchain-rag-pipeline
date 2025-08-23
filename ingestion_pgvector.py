import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

# Import the PDF loader function
from pdf_loader import load_and_split_pdf

def ingest_to_pgvector(splits=None):
    """
    Ingest chunked documents into PGVector database.
    
    Args:
        splits: List of Document objects. If None, loads and splits PDF first.
    
    Returns:
        PGVector store instance
    """
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Missing required environment variable: {var}")
    
    # If no splits provided, load and split PDF
    if splits is None:
        print("No splits provided, loading and splitting PDF...")
        splits = load_and_split_pdf()
        
        if not splits:
            raise RuntimeError("Failed to load and split PDF")
    
    # Clean and enrich documents
    enriched = []
    for i, doc in enumerate(splits):
        # Filter out empty or None metadata values
        meta = {k: v for k, v in doc.metadata.items() if v not in ("", None)}
        
        # Add chunk index to metadata
        meta['chunk_index'] = i
        
        new_doc = Document(
            page_content=doc.page_content,
            metadata=meta
        )
        enriched.append(new_doc)
    
    print(f"Prepared {len(enriched)} enriched documents for ingestion")
    
    # Generate unique IDs for documents
    ids = [f"doc-{i}" for i in range(len(enriched))]
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
    )
    
    # Initialize PGVector store
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    
    print("Adding documents to PGVector...")
    
    # Add documents to the vector store
    store.add_documents(documents=enriched, ids=ids)
    
    print(f"Successfully ingested {len(enriched)} documents into PGVector")
    print(f"Collection: {os.getenv('PGVECTOR_COLLECTION')}")
    
    return store

if __name__ == "__main__":
    try:
        store = ingest_to_pgvector()
        print("Ingestion completed successfully!")
    except Exception as e:
        print(f"Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
