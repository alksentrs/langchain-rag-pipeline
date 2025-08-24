# LangChain RAG Pipeline with PGVector + MCP Integration

This project demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline using LangChain and PGVector, with **Model Context Protocol (MCP)** integration for seamless use with Cursor and other AI tools. It shows how to:

1. **Load PDF content** and split it into chunks with overlap
2. **Ingest chunks** into a PGVector database with vector embeddings
3. **Perform similarity search** with scoring on the vector database
4. **🆕 Access via MCP** - Query your knowledge base directly from Cursor!

## 🏗️ Architecture

The project consists of several Python scripts that work together:

### Core RAG Pipeline
- **`pdf_loader.py`** - Loads PDF files and splits text into chunks
- **`ingestion_pgvector.py`** - Ingests chunked documents into PGVector
- **`search_vector.py`** - Performs vector similarity search
- **`main.py`** - Orchestrates the complete pipeline

### 🆕 MCP Integration
- **`mcp_server.py`** - MCP server providing RAG capabilities to AI tools
- **`mcp_client_example.py`** - Example client showing MCP usage
- **`test_mcp_integration.py`** - Comprehensive MCP testing suite
- **`.cursorrules`** - Cursor configuration for MCP integration

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
python3 -m venv venv
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

## 🔗 MCP Integration (NEW!)

### What is MCP?
Model Context Protocol (MCP) allows AI tools like Cursor to interact with your RAG pipeline directly. You can now ask Cursor questions about your documents!

### Quick MCP Setup

1. **Start the MCP server**:
   ```bash
   python mcp_server.py
   ```

2. **Configure Cursor**: The `.cursorrules` file is already configured for MCP integration.

3. **Test the integration**:
   ```bash
   python test_mcp_integration.py
   ```

### MCP Tools Available

#### 🔍 `rag_search`
Search your knowledge base using natural language:
```json
{
  "tool": "rag_search",
  "arguments": {
    "query": "What are the performance improvements in GPT-5?",
    "k": 3
  }
}
```

#### 📄 `rag_ingest_pdf`
Add new documents to your knowledge base:
```json
{
  "tool": "rag_ingest_pdf", 
  "arguments": {
    "pdf_path": "./documents/research_paper.pdf",
    "chunk_size": 1000,
    "chunk_overlap": 150
  }
}
```

#### 📊 `rag_get_stats`
Check system status and configuration:
```json
{
  "tool": "rag_get_stats",
  "arguments": {}
}
```

### Using with Cursor

Once the MCP server is running, you can interact with your RAG system directly in Cursor:

- **"Search my knowledge base for information about machine learning performance"**
- **"What does my document collection say about GPT-5 improvements?"**  
- **"Ingest the new research paper into my knowledge base"**
- **"Show me the current status of my RAG system"**

### MCP Resources

- **`rag://status`** - System status and configuration
- **`rag://search`** - Search interface documentation  
- **`rag://help`** - Complete help and usage guide

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

### Core RAG Pipeline Testing

You can test individual components:

```bash
# Test PDF loading only
python pdf_loader.py

# Test ingestion only
python ingestion_pgvector.py

# Test search only
python search_vector.py

# Test complete pipeline
python main.py
```

### 🆕 MCP Integration Testing

Test the MCP server and integration:

```bash
# Comprehensive MCP integration test
python test_mcp_integration.py

# Interactive MCP client demo
python mcp_client_example.py --interactive

# Basic MCP client demo
python mcp_client_example.py
```

### MCP Testing Scenarios

1. **Environment Check**: Verifies all required environment variables
2. **Search Without Documents**: Tests search functionality on empty database
3. **PDF Ingestion**: Tests document ingestion capabilities
4. **Search With Documents**: Tests search after ingestion
5. **System Statistics**: Tests status and configuration retrieval

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

4. **🆕 MCP Server Issues**
   - Ensure MCP dependencies are installed: `pip install mcp`
   - Check if server starts: `python mcp_server.py`
   - Verify Cursor can connect to the MCP server
   - Test with: `python test_mcp_integration.py`

5. **🆕 Cursor Integration Issues**
   - Check `.cursorrules` file is present
   - Ensure MCP server is running before using Cursor
   - Verify MCP configuration in `mcp_config.json`

### Debug Mode

Add debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -u main.py
```

## 📚 Dependencies

### Core RAG Pipeline
- **LangChain**: Core RAG framework
- **OpenAI**: Embeddings and language models
- **PGVector**: Vector database extension
- **PyPDF**: PDF document processing
- **psycopg2**: PostgreSQL adapter

### 🆕 MCP Integration
- **MCP**: Model Context Protocol implementation
- **Pydantic**: Data validation and serialization
- **FastAPI**: Web framework for API endpoints
- **Uvicorn**: ASGI server for running the MCP server

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
