#!/usr/bin/env python3
"""
Simple script to ingest gato_especial.pdf into the vector database
"""

from pdf_loader import load_and_split_pdf
from ingestion_pgvector import ingest_to_pgvector

def main():
    print("🚀 Starting ingestion of gato_especial.pdf...")
    
    # Load and split the PDF
    print("📖 Loading and splitting PDF...")
    splits = load_and_split_pdf(pdf_path='data/gato_especial.pdf')
    print(f"✅ Created {len(splits)} chunks")
    
    # Ingest into vector database
    print("🗄️ Ingesting into vector database...")
    store = ingest_to_pgvector(splits)
    print("🎉 Successfully ingested gato_especial.pdf into vector database!")
    
    return store

if __name__ == "__main__":
    main()
