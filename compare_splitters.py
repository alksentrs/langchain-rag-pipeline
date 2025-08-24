#!/usr/bin/env python3
"""
Compare old vs new PDF splitting methods
"""

from pdf_loader import load_and_split_pdf
from smart_pdf_splitter import load_and_split_pdf_smart

def compare_splitting_methods(pdf_path: str):
    """Compare the old and new splitting methods."""
    
    print("🔄 Comparing PDF Splitting Methods")
    print("=" * 60)
    
    # Method 1: Old RecursiveCharacterTextSplitter
    print("\n📖 Method 1: RecursiveCharacterTextSplitter (Old)")
    print("-" * 50)
    try:
        old_chunks = load_and_split_pdf(pdf_path)
        print(f"✅ Created {len(old_chunks)} chunks")
        
        # Show sample chunks
        for i, chunk in enumerate(old_chunks[:2]):
            print(f"\n--- Old Chunk {i+1} ---")
            print(f"Size: {len(chunk.page_content)} characters")
            print(f"Content: {chunk.page_content[:150]}...")
            
    except Exception as e:
        print(f"❌ Error with old method: {e}")
    
    # Method 2: New Smart Splitter
    print("\n🧠 Method 2: SmartPDFSplitter (New)")
    print("-" * 50)
    try:
        new_chunks = load_and_split_pdf_smart(pdf_path)
        print(f"✅ Created {len(new_chunks)} chunks")
        
        # Show sample chunks
        for i, chunk in enumerate(new_chunks[:2]):
            print(f"\n--- New Chunk {i+1} ---")
            print(f"Size: {len(chunk.page_content)} characters")
            print(f"Content: {chunk.page_content[:150]}...")
            
    except Exception as e:
        print(f"❌ Error with new method: {e}")
    
    # Analysis
    print("\n📊 Analysis:")
    print("=" * 60)
    
    if 'old_chunks' in locals() and 'new_chunks' in locals():
        print(f"Old method chunks: {len(old_chunks)}")
        print(f"New method chunks: {len(new_chunks)}")
        
        # Analyze chunk quality
        old_sizes = [len(chunk.page_content) for chunk in old_chunks]
        new_sizes = [len(chunk.page_content) for chunk in new_chunks]
        
        print(f"\nOld method - Avg size: {sum(old_sizes)/len(old_sizes):.0f} chars")
        print(f"New method - Avg size: {sum(new_sizes)/len(new_sizes):.0f} chars")
        
        print(f"\nOld method - Size range: {min(old_sizes)} to {max(old_sizes)} chars")
        print(f"New method - Size range: {min(new_sizes)} to {max(new_sizes)} chars")
        
        # Check for sentence breaks
        old_mid_sentence = sum(1 for chunk in old_chunks if not chunk.page_content.strip().endswith(('.', '!', '?')))
        new_mid_sentence = sum(1 for chunk in new_chunks if not chunk.page_content.strip().endswith(('.', '!', '?')))
        
        print(f"\nOld method - Chunks ending mid-sentence: {old_mid_sentence}")
        print(f"New method - Chunks ending mid-sentence: {new_mid_sentence}")
        
        print(f"\nOld method - % complete sentences: {((len(old_chunks) - old_mid_sentence) / len(old_chunks) * 100):.1f}%")
        print(f"New method - % complete sentences: {((len(new_chunks) - new_mid_sentence) / len(new_chunks) * 100):.1f}%")

if __name__ == "__main__":
    pdf_path = "data/gato_especial.pdf"
    compare_splitting_methods(pdf_path)
