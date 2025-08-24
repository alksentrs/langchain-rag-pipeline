# 🧠 Smart PDF Splitter

## Overview
The Smart PDF Splitter is an advanced document chunking system that respects natural language boundaries, providing much better semantic coherence than traditional character-based splitters.

## 🚀 Key Features

### **Natural Language Boundary Detection**
- **Sentence Boundaries**: Respects periods, exclamation marks, and question marks
- **Paragraph Breaks**: Preserves paragraph structure
- **Semantic Coherence**: Maintains logical flow within chunks
- **Multi-language Support**: Optimized for Portuguese and English

### **Intelligent Break Point Selection**
- **Scoring System**: Evaluates break points based on distance and quality
- **Abbreviation Detection**: Avoids breaking on common abbreviations (Dr., Sr., etc.)
- **Fallback Strategies**: Multiple break strategies for optimal results
- **Configurable Parameters**: Adjustable chunk sizes and overlap

### **Quality Analysis**
- **Chunk Statistics**: Size distribution and analysis
- **Boundary Quality**: Percentage of complete sentences
- **Performance Metrics**: Comparison with traditional methods

## 🔧 How It Works

### **1. Text Cleaning**
```python
# Remove excessive whitespace
# Normalize line breaks
# Clean up punctuation spacing
# Remove page numbers and headers
```

### **2. Boundary Detection**
```python
# Sentence endings (.!?)
# Paragraph breaks (\n\n)
# Comma and semicolon breaks
# Abbreviation filtering
```

### **3. Smart Break Selection**
```python
# Score-based selection
# Distance optimization
# Quality prioritization
# Fallback strategies
```

## 📊 Comparison with Traditional Methods

| Aspect | RecursiveCharacterTextSplitter | SmartPDFSplitter |
|--------|--------------------------------|------------------|
| **Sentence Completion** | ~54.5% | ~68.8% |
| **Chunk Coherence** | Low | High |
| **Boundary Respect** | None | Full |
| **Semantic Flow** | Broken | Preserved |
| **Language Support** | Basic | Multi-language |

## 🎯 Usage Examples

### **Basic Usage**
```python
from smart_pdf_splitter import load_and_split_pdf_smart

# Load and split PDF
chunks = load_and_split_pdf_smart(
    pdf_path='document.pdf',
    chunk_size=1000,
    chunk_overlap=150
)
```

### **Advanced Usage**
```python
from smart_pdf_splitter import SmartPDFSplitter

# Create custom splitter
splitter = SmartPDFSplitter(
    chunk_size=800,
    chunk_overlap=200,
    min_chunk_size=300,
    max_chunk_size=1500
)

# Split PDF
chunks = splitter.split_pdf_smart('document.pdf')

# Analyze results
analysis = splitter.analyze_chunks(chunks)
```

### **Integration with RAG System**
```python
# Use in ingestion pipeline
from smart_pdf_splitter import load_and_split_pdf_smart
from ingestion_pgvector import ingest_to_pgvector

# Smart splitting + ingestion
splits = load_and_split_pdf_smart('document.pdf')
store = ingest_to_pgvector(splits)
```

## ⚙️ Configuration Options

### **Chunk Parameters**
```python
chunk_size = 1000        # Target chunk size (characters)
chunk_overlap = 150      # Overlap between chunks
min_chunk_size = 200     # Minimum acceptable size
max_chunk_size = 2000    # Maximum acceptable size
```

### **Boundary Detection**
```python
# Sentence endings (Portuguese + English)
sentence_endings = r'[.!?]+["\']*\s+'

# Paragraph breaks
paragraph_breaks = r'\n\s*\n+'

# Common abbreviations
abbreviations = {'Dr.', 'Sr.', 'Sra.', 'Prof.', 'etc.'}
```

## 🔍 Quality Metrics

### **Chunk Analysis**
```python
analysis = {
    'total_chunks': 32,
    'avg_chunk_size': 835,
    'min_chunk_size': 307,
    'max_chunk_size': 1141,
    'size_distribution': {
        'small': 6,      # < 500 chars
        'medium': 14,    # 500-1000 chars
        'large': 12      # > 1000 chars
    }
}
```

### **Boundary Quality**
- **Complete Sentences**: Chunks ending with proper punctuation
- **Mid-sentence Breaks**: Chunks cut mid-thought
- **Semantic Coherence**: Logical flow preservation

## 🚀 Performance Benefits

### **For RAG Systems**
- **Better Search Results**: More coherent chunks improve vector search
- **Improved AI Responses**: Cleaner context for language models
- **Reduced Noise**: Fewer broken sentences and incomplete thoughts

### **For Document Processing**
- **Maintains Structure**: Preserves document organization
- **Language Agnostic**: Works with multiple languages
- **Configurable**: Adapts to different document types

## 🔧 Advanced Features

### **Custom Boundary Detection**
```python
class CustomSplitter(SmartPDFSplitter):
    def __init__(self):
        super().__init__()
        # Add custom abbreviations
        self.abbreviations.update({'custom', 'abbr'})
        
        # Custom sentence patterns
        self.sentence_endings = r'[.!?;]+["\']*\s+'
```

### **Batch Processing**
```python
# Process multiple documents
documents = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']
all_chunks = []

for doc in documents:
    chunks = load_and_split_pdf_smart(doc)
    all_chunks.extend(chunks)
```

## 📈 Best Practices

### **Chunk Size Selection**
- **Small Documents**: 500-800 characters
- **Medium Documents**: 800-1200 characters
- **Large Documents**: 1200-2000 characters

### **Overlap Configuration**
- **High Precision**: 200-300 characters overlap
- **Balanced**: 150-200 characters overlap
- **Efficiency**: 100-150 characters overlap

### **Language Considerations**
- **Portuguese**: Respects Portuguese punctuation and abbreviations
- **English**: Optimized for English sentence structure
- **Mixed**: Handles documents with multiple languages

## 🔍 Troubleshooting

### **Common Issues**

1. **Too Many Small Chunks**
   - Increase `min_chunk_size`
   - Reduce `chunk_overlap`

2. **Chunks Too Large**
   - Decrease `chunk_size`
   - Increase `chunk_overlap`

3. **Poor Boundary Detection**
   - Check document formatting
   - Adjust abbreviation list
   - Verify language settings

### **Debug Mode**
```python
# Enable detailed logging
splitter = SmartPDFSplitter()
chunks = splitter.split_pdf_smart('document.pdf')

# Analyze results
analysis = splitter.analyze_chunks(chunks)
print(analysis)
```

## 🚀 Future Enhancements

### **Planned Features**
- **Semantic Chunking**: AI-powered content-aware splitting
- **Multi-format Support**: DOCX, TXT, HTML support
- **Custom Rules Engine**: User-defined splitting rules
- **Performance Optimization**: Parallel processing for large documents

### **Integration Opportunities**
- **LangChain Ecosystem**: Native LangChain integration
- **Vector Databases**: Optimized for PGVector, Chroma, etc.
- **AI Models**: Enhanced context for LLM processing

## 📚 Files

- **`smart_pdf_splitter.py`** - Main smart splitter implementation
- **`compare_splitters.py`** - Comparison with traditional methods
- **`ingest_smart_gato_especial.py`** - Smart ingestion example
- **`SMART_SPLITTER_README.md`** - This documentation

## 🤝 Contributing

### **Improvement Areas**
- **Language Support**: Add more language-specific rules
- **Boundary Detection**: Enhance sentence boundary algorithms
- **Performance**: Optimize for large document processing
- **Testing**: Add comprehensive test suite

### **Testing**
```bash
# Test the smart splitter
python3 smart_pdf_splitter.py

# Compare with traditional method
python3 compare_splitters.py

# Test smart ingestion
python3 ingest_smart_gato_especial.py
```

---

**Transform your document processing with intelligent, semantic-aware chunking! 🎉**
