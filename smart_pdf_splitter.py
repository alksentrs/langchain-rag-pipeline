#!/usr/bin/env python3
"""
Smart PDF Splitter with Natural Language Boundary Detection
Respects sentences, paragraphs, and semantic coherence
"""

import re
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class SmartPDFSplitter:
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 150,
                 min_chunk_size: int = 200,
                 max_chunk_size: int = 2000):
        """
        Initialize the smart PDF splitter.
        
        Args:
            chunk_size: Target size for chunks (characters)
            chunk_overlap: Overlap between chunks (characters)
            min_chunk_size: Minimum acceptable chunk size
            max_chunk_size: Maximum acceptable chunk size
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        
        # Sentence ending patterns (Portuguese + English)
        self.sentence_endings = r'[.!?]+["\']*\s+'
        
        # Paragraph break patterns
        self.paragraph_breaks = r'\n\s*\n+'
        
        # Common abbreviations that shouldn't end sentences
        self.abbreviations = {
            'Dr.', 'Sr.', 'Sra.', 'Prof.', 'etc.', 'vs.', 'i.e.', 'e.g.',
            'pág.', 'p.', 'cap.', 'vol.', 'ed.', 'nº', 'n°', 'art.',
            'inc.', 'corp.', 'co.', 'ltd.', 'llc.', 'inc', 'corp'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for better splitting.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        # Remove page numbers and headers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([.!?])', r'\1', text)
        text = re.sub(r'([.!?])\s*', r'\1 ', text)
        
        return text.strip()
    
    def is_sentence_boundary(self, text: str, pos: int) -> bool:
        """
        Check if a position represents a true sentence boundary.
        
        Args:
            text: Full text
            pos: Position to check
            
        Returns:
            True if it's a sentence boundary
        """
        if pos >= len(text) - 1:
            return True
            
        # Look for sentence ending patterns
        match = re.search(self.sentence_endings, text[pos:pos+10])
        if not match:
            return False
            
        # Check if it's not an abbreviation
        before_text = text[max(0, pos-30):pos+1]
        for abbr in self.abbreviations:
            if abbr in before_text:
                return False
        
        # Additional checks for better accuracy
        # Look ahead to see if next character is uppercase (likely new sentence)
        if pos + 1 < len(text):
            next_char = text[pos + 1]
            if next_char.isupper() and next_char.isalpha():
                return True
        
        # Check if followed by whitespace and uppercase letter
        if pos + 2 < len(text):
            if text[pos + 1].isspace() and text[pos + 2].isupper():
                return True
                
        return True
    
    def find_smart_break(self, text: str, target_pos: int) -> int:
        """
        Find the best position to break text, respecting sentence boundaries.
        
        Args:
            text: Text to split
            target_pos: Target position for splitting
            
        Returns:
            Best position to break
        """
        # Look for sentence boundaries near target position
        search_start = max(0, target_pos - 150)
        search_end = min(len(text), target_pos + 150)
        
        best_break = target_pos
        best_score = float('inf')
        
        # Search for sentence endings with scoring
        for i in range(search_start, search_end):
            if self.is_sentence_boundary(text, i):
                # Calculate score based on distance and quality
                distance = abs(i - target_pos)
                score = distance
                
                # Bonus for being closer to target
                if distance <= 50:
                    score *= 0.5
                elif distance <= 100:
                    score *= 0.8
                
                # Bonus for sentence endings vs other breaks
                if text[i] in '.!?':
                    score *= 0.7
                
                if score < best_score:
                    best_score = score
                    best_break = i
        
        # If no good sentence boundary found, look for paragraph breaks
        if best_break == target_pos:
            for i in range(search_start, search_end):
                if text[i:i+2] == '\n\n':
                    distance = abs(i - target_pos)
                    if distance <= 100:
                        best_break = i
                        break
        
        # If still no good break, look for commas or other punctuation
        if best_break == target_pos:
            for i in range(search_start, search_end):
                if text[i] in ',;:':
                    distance = abs(i - target_pos)
                    if distance <= 100:
                        best_break = i
                        break
        
        return best_break
    
    def split_text_smart(self, text: str) -> List[str]:
        """
        Split text into chunks while respecting natural language boundaries.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate target end position
            end = start + self.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunk = text[start:].strip()
                if chunk and len(chunk) >= self.min_chunk_size:
                    chunks.append(chunk)
                break
            
            # Find smart break point
            break_pos = self.find_smart_break(text, end)
            
            # Extract chunk
            chunk = text[start:break_pos].strip()
            
            if chunk and len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)
            
            # Update start position with overlap
            start = max(start + 1, break_pos - self.chunk_overlap)
            
            # Safety check to prevent infinite loops
            if start >= len(text):
                break
        
        return chunks
    
    def split_pdf_smart(self, pdf_path: str) -> List[Document]:
        """
        Load and split PDF using smart splitting strategy.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of Document objects
        """
        print(f"Loading PDF from: {pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        print(f"Loaded {len(pages)} pages from PDF")
        
        all_chunks = []
        
        for page in pages:
            # Clean text
            clean_text = self.clean_text(page.page_content)
            
            # Split text smartly
            text_chunks = self.split_text_smart(clean_text)
            
            # Create Document objects
            for i, chunk in enumerate(text_chunks):
                # Create metadata
                metadata = page.metadata.copy()
                metadata['chunk_index'] = i
                metadata['chunk_size'] = len(chunk)
                metadata['split_method'] = 'smart_splitter'
                
                # Create Document
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                all_chunks.append(doc)
        
        print(f"Created {len(all_chunks)} smart chunks")
        print(f"Chunk size: {self.chunk_size} characters")
        print(f"Chunk overlap: {self.chunk_overlap} characters")
        print(f"Min chunk size: {self.min_chunk_size} characters")
        print(f"Max chunk size: {self.max_chunk_size} characters")
        
        return all_chunks
    
    def analyze_chunks(self, chunks: List[Document]) -> Dict[str, Any]:
        """
        Analyze the quality of generated chunks.
        
        Args:
            chunks: List of Document chunks
            
        Returns:
            Analysis results
        """
        if not chunks:
            return {}
        
        sizes = [len(chunk.page_content) for chunk in chunks]
        
        analysis = {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(sizes) / len(sizes),
            'min_chunk_size': min(sizes),
            'max_chunk_size': max(sizes),
            'size_distribution': {
                'small': len([s for s in sizes if s < 500]),
                'medium': len([s for s in sizes if 500 <= s <= 1000]),
                'large': len([s for s in sizes if s > 1000])
            }
        }
        
        return analysis

def load_and_split_pdf_smart(pdf_path: str, 
                           chunk_size: int = 1000,
                           chunk_overlap: int = 150) -> List[Document]:
    """
    Convenience function for smart PDF loading and splitting.
    
    Args:
        pdf_path: Path to PDF file
        chunk_size: Target chunk size
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of Document objects
    """
    splitter = SmartPDFSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    return splitter.split_pdf_smart(pdf_path)

if __name__ == "__main__":
    # Example usage
    pdf_path = "data/gato_especial.pdf"
    
    try:
        # Load and split PDF
        chunks = load_and_split_pdf_smart(pdf_path)
        
        # Analyze chunks
        splitter = SmartPDFSplitter()
        analysis = splitter.analyze_chunks(chunks)
        
        print("\n📊 Chunk Analysis:")
        print("=" * 40)
        for key, value in analysis.items():
            if key == 'size_distribution':
                print(f"{key}:")
                for size_key, size_value in value.items():
                    print(f"  {size_key}: {size_value}")
            else:
                print(f"{key}: {value}")
        
        # Show sample chunks
        print(f"\n🔍 Sample Chunks:")
        print("=" * 40)
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Size: {len(chunk.page_content)} characters")
            print(f"Content Preview: {chunk.page_content[:200]}...")
            print(f"Metadata: {chunk.metadata}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
