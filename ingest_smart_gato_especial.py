#!/usr/bin/env python3
"""
Smart ingestion script using the improved PDF splitter
"""

from smart_pdf_splitter import load_and_split_pdf_smart
from ingestion_pgvector import ingest_to_pgvector

def main():
    print("🚀 Starting SMART ingestion of gato_especial.pdf...")
    
    # Load and split the PDF using smart splitting
    print("📖 Loading and splitting PDF with smart boundaries...")
    splits = load_and_split_pdf_smart(
        pdf_path='data/gato_especial.pdf',
        chunk_size=1000,      # Target chunk size
        chunk_overlap=150     # Overlap between chunks
    )
    print(f"✅ Created {len(splits)} smart chunks")
    
    # Ingest into vector database
    print("🗄️ Ingesting into vector database...")
    store = ingest_to_pgvector(splits)
    print("🎉 Successfully ingested gato_especial.pdf with SMART splitting!")
    
    return store

if __name__ == "__main__":
    main()
