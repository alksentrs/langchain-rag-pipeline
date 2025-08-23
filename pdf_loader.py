import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_and_split_pdf(pdf_path: str = None, chunk_size: int = 1000, chunk_overlap: int = 150):
    """
    Load a PDF file and split it into chunks with overlap.
    
    Args:
        pdf_path: Path to the PDF file. If None, looks for 'gpt5.pdf' in the same directory.
        chunk_size: Size of each text chunk in characters
        chunk_overlap: Overlap between consecutive chunks in characters
    
    Returns:
        List of Document objects with chunked content
    """
    # Load environment variables
    load_dotenv()
    
    # If no PDF path provided, look for gpt5.pdf in the same directory
    if pdf_path is None:
        current_dir = Path(__file__).parent
        pdf_path = current_dir / "gpt5.pdf"
    
    print(f"Loading PDF from: {pdf_path}")
    
    # Load PDF content
    try:
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        print(f"Loaded {len(docs)} pages from PDF")
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=False
    )
    
    splits = text_splitter.split_documents(docs)
    
    if not splits:
        print("No splits generated. Exiting.")
        return []
    
    print(f"Created {len(splits)} text chunks")
    print(f"Chunk size: {chunk_size} characters")
    print(f"Chunk overlap: {chunk_overlap} characters")
    
    # Print first few chunks as preview
    for i, split in enumerate(splits[:3]):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Content preview: {split.page_content[:100]}...")
        print(f"Metadata: {split.metadata}")
    
    return splits

if __name__ == "__main__":
    # Example usage
    splits = load_and_split_pdf()
    print(f"\nTotal chunks created: {len(splits)}")
