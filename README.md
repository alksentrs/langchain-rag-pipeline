# LangChain RAG Pipeline with PGVector

This project demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline using LangChain and PGVector. It shows how to:

1. **Load PDF content** and split it into chunks with overlap
2. **Ingest chunks** into a PGVector database with vector embeddings
3. **Perform similarity search** with scoring on the vector database

## 🏗️ Architecture

The project consists of several Python scripts that work together:

- **`pdf_loader.py`** - Loads PDF files and splits text into chunks
- **`ingestion_pgvector.py`** - Ingests chunked documents into PGVector
- **`search_vector.py`** - Performs vector similarity search
- **`main.py`** - Orchestrates the complete pipeline

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your OpenAI API key
nano .env
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=text-embedding-3-small
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=langchain_pg_embedding
```

### 3. Start PostgreSQL with pgvector

```bash
# Start the database
docker-compose up -d

# Wait for database to be ready (check logs)
docker-compose logs -f postgres
```

### 4. Add Your PDF

Place a PDF file named `gpt5.pdf` in the project root directory.

### 5. Run the Pipeline

```bash
# Run the complete pipeline
python main.py
```

## 📖 Individual Scripts

### PDF Loader (`pdf_loader.py`)

```python
from pdf_loader import load_and_split_pdf

# Load and split PDF with custom parameters
splits = load_and_split_pdf(
    pdf_path="your_document.pdf",
    chunk_size=1000,
    chunk_overlap=150
)
```

### PGVector Ingestion (`ingestion_pgvector.py`)

```python
from ingestion_pgvector import ingest_to_pgvector

# Ingest pre-split documents
store = ingest_to_pgvector(splits)

# Or let it load and split automatically
store = ingest_to_pgvector()
```

### Vector Search (`search_vector.py`)

```python
from search_vector import search_vector_database, display_search_results

# Perform similarity search
results = search_vector_database("Your search query", k=5)

# Display results
display_search_results(results)
```

## 🔧 Configuration

### Chunking Parameters

- **Chunk Size**: Default 1000 characters
- **Chunk Overlap**: Default 150 characters
- **Text Splitter**: RecursiveCharacterTextSplitter

### Vector Database

- **Database**: PostgreSQL 16 with pgvector extension
- **Collection**: `langchain_pg_embedding`
- **Metadata**: Stored as JSONB for flexibility

### Embeddings

- **Model**: OpenAI text-embedding-3-small (default)
- **Vector Dimension**: 1536 (model-dependent)

## 🐳 Docker Setup

The project includes a `docker-compose.yaml` file that sets up:

- PostgreSQL 16 with pgvector extension
- Database: `rag`
- User: `postgres`
- Password: `postgres`
- Port: `5432`

## 📊 Example Output

```
🚀 Starting LangChain RAG Pipeline
==================================================

📖 Step 1: Loading and splitting PDF...
Loading PDF from: gpt5.pdf
Loaded 15 pages from PDF
Created 47 text chunks
Chunk size: 1000 characters
Chunk overlap: 150 characters
✅ Successfully created 47 text chunks

🗄️  Step 2: Ingesting into PGVector database...
Prepared 47 enriched documents for ingestion
Adding documents to PGVector...
Successfully ingested 47 documents into PGVector
Collection: langchain_pg_embedding
✅ Successfully ingested documents into PGVector

🔍 Step 3: Performing vector similarity search...

--- Search Query 1 ---
Query: Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4
Searching for: 'Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4'
Returning top 3 results...

Found 3 results:
==================================================
Result 1 (score: 0.1234):
==================================================

Content:
------------------------------
[Document content here...]

Metadata:
------------------------------
page: 1
chunk_index: 0
source: gpt5.pdf
```

## 🧪 Testing

You can test individual components:

```bash
# Test PDF loading only
python pdf_loader.py

# Test ingestion only
python ingestion_pgvector.py

# Test search only
python search_vector.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure Docker is running
   - Check if PostgreSQL container is up: `docker-compose ps`
   - Verify connection string in `.env`

2. **OpenAI API Error**
   - Verify your API key is correct
   - Check API quota and billing
   - Ensure model name is valid

3. **PDF Loading Error**
   - Verify PDF file exists and is readable
   - Check if PyPDF is properly installed
   - Ensure PDF is not corrupted

### Debug Mode

Add debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -u main.py
```

## 📚 Dependencies

- **LangChain**: Core RAG framework
- **OpenAI**: Embeddings and language models
- **PGVector**: Vector database extension
- **PyPDF**: PDF document processing
- **psycopg2**: PostgreSQL adapter

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain team for the excellent framework
- PGVector contributors for the vector database extension
- OpenAI for the embedding models
