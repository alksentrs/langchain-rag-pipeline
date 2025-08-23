import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

def search_vector_database(query, k=3):
    """
    Perform similarity search on the PGVector database.
    
    Args:
        query: Search query string
        k: Number of top results to return
    
    Returns:
        List of (document, score) tuples
    """
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Missing required environment variable: {var}")
    
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
    
    print(f"Searching for: '{query}'")
    print(f"Returning top {k} results...")
    
    # Perform similarity search with scores
    results = store.similarity_search_with_score(query, k=k)
    
    return results

def display_search_results(results):
    """
    Display search results in a formatted way.
    
    Args:
        results: List of (document, score) tuples
    """
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} results:")
    
    for i, (doc, score) in enumerate(results, start=1):
        print("="*50)
        print(f"Result {i} (score: {score:.4f}):")
        print("="*50)
        
        print("\nContent:")
        print("-" * 30)
        print(doc.page_content.strip())
        
        print("\nMetadata:")
        print("-" * 30)
        for key, value in doc.metadata.items():
            print(f"{key}: {value}")
        
        print()

if __name__ == "__main__":
    # Example search query
    query = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"
    
    try:
        # Perform the search
        results = search_vector_database(query, k=3)
        
        # Display results
        display_search_results(results)
        
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
