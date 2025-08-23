#!/usr/bin/env python3
"""
Main script for the LangChain RAG pipeline.
This script demonstrates the complete workflow:
1. Load and split PDF content
2. Ingest chunks into PGVector database
3. Perform vector similarity search
"""

import os
from dotenv import load_dotenv
from pdf_loader import load_and_split_pdf
from ingestion_pgvector import ingest_to_pgvector
from search_vector import search_vector_database, display_search_results

def main():
    """
    Main function that runs the complete RAG pipeline.
    """
    print("🚀 Starting LangChain RAG Pipeline")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if we have a PDF file
    pdf_path = "gpt5.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file '{pdf_path}' not found!")
        print("Please place a PDF file named 'gpt5.pdf' in the current directory.")
        return
    
    try:
        # Step 1: Load and split PDF
        print("\n📖 Step 1: Loading and splitting PDF...")
        splits = load_and_split_pdf(pdf_path)
        
        if not splits:
            print("❌ Failed to load and split PDF. Exiting.")
            return
        
        print(f"✅ Successfully created {len(splits)} text chunks")
        
        # Step 2: Ingest into PGVector
        print("\n🗄️  Step 2: Ingesting into PGVector database...")
        store = ingest_to_pgvector(splits)
        print("✅ Successfully ingested documents into PGVector")
        
        # Step 3: Perform vector search
        print("\n🔍 Step 3: Performing vector similarity search...")
        
        # Example search queries
        queries = [
            "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4",
            "What are the key improvements in GPT-5?",
            "How does GPT-5 perform in reasoning tasks?"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\n--- Search Query {i} ---")
            print(f"Query: {query}")
            
            results = search_vector_database(query, k=3)
            display_search_results(results)
        
        print("\n🎉 RAG Pipeline completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in RAG pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
