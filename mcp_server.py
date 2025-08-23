#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for the LangChain RAG Pipeline.
This server allows Cursor and other MCP clients to interact with your RAG system.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    ReadResourceResult,
)

# Import our RAG pipeline components
try:
    from pdf_loader import load_and_split_pdf
    from ingestion_pgvector import ingest_to_pgvector
    from search_vector import search_vector_database
except ImportError as e:
    print(f"Error importing RAG components: {e}")
    print("Make sure all RAG pipeline files are in the same directory")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("rag-pipeline")

class RAGManager:
    """Manages RAG operations for the MCP server."""
    
    def __init__(self):
        self.vector_store = None
        self.is_initialized = False
        self.last_ingestion_info = None
    
    async def search_documents(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Search the RAG vector database."""
        try:
            logger.info(f"Searching for: {query} (k={k})")
            results = search_vector_database(query, k=k)
            
            # Format results for MCP
            formatted_results = []
            for i, (doc, score) in enumerate(results, 1):
                formatted_results.append({
                    "rank": i,
                    "score": float(score),
                    "content": doc.page_content.strip()[:500] + "..." if len(doc.page_content) > 500 else doc.page_content.strip(),
                    "full_content": doc.page_content.strip(),
                    "metadata": doc.metadata
                })
            
            return {
                "success": True,
                "query": query,
                "results_count": len(formatted_results),
                "results": formatted_results
            }
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return {
                "error": f"Search failed: {str(e)}",
                "success": False
            }
    
    async def ingest_pdf(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> Dict[str, Any]:
        """Ingest a PDF file into the vector database."""
        try:
            logger.info(f"Ingesting PDF: {pdf_path}")
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                return {"error": f"PDF file not found: {pdf_path}", "success": False}
            
            # Load and split PDF
            splits = load_and_split_pdf(pdf_path, chunk_size, chunk_overlap)
            
            if not splits:
                return {"error": "Failed to load and split PDF", "success": False}
            
            # Ingest into vector database
            store = ingest_to_pgvector(splits)
            self.vector_store = store
            self.is_initialized = True
            
            # Store ingestion info
            self.last_ingestion_info = {
                "pdf_path": pdf_path,
                "chunks_created": len(splits),
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            }
            
            return {
                "success": True,
                "pdf_path": pdf_path,
                "chunks_created": len(splits),
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "message": f"Successfully ingested {len(splits)} chunks from {os.path.basename(pdf_path)}"
            }
            
        except Exception as e:
            logger.error(f"Ingestion failed: {str(e)}")
            return {
                "error": f"Ingestion failed: {str(e)}",
                "success": False
            }
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        try:
            # Check environment variables
            env_status = {
                "openai_api_key": "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
                "pgvector_url": "✅ Set" if os.getenv("PGVECTOR_URL") else "❌ Missing",
                "pgvector_collection": "✅ Set" if os.getenv("PGVECTOR_COLLECTION") else "❌ Missing"
            }
            
            # Check if vector store is initialized
            store_status = "✅ Initialized" if self.is_initialized else "❌ Not initialized"
            
            # Get collection name
            collection_name = os.getenv("PGVECTOR_COLLECTION", "langchain_pg_embedding")
            
            result = {
                "success": True,
                "environment": env_status,
                "vector_store": store_status,
                "collection_name": collection_name,
                "server_status": "✅ Running"
            }
            
            # Add last ingestion info if available
            if self.last_ingestion_info:
                result["last_ingestion"] = self.last_ingestion_info
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {
                "error": f"Failed to get stats: {str(e)}",
                "success": False
            }

# Initialize RAG manager
rag_manager = RAGManager()

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="rag://status",
            name="RAG System Status",
            description="Current status of the RAG system including environment and database state",
            mimeType="application/json"
        ),
        Resource(
            uri="rag://search",
            name="RAG Search Interface",
            description="Interface for searching the vector database",
            mimeType="application/json"
        ),
        Resource(
            uri="rag://help",
            name="RAG Help",
            description="Help and usage information for the RAG system",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read resource content."""
    if uri == "rag://status":
        stats = await rag_manager.get_system_stats()
        return json.dumps(stats, indent=2)
    elif uri == "rag://search":
        return json.dumps({
            "message": "Use the rag_search tool to search the vector database",
            "example": {
                "tool": "rag_search",
                "arguments": {
                    "query": "your search query here",
                    "k": 3
                }
            }
        }, indent=2)
    elif uri == "rag://help":
        return """RAG Pipeline MCP Server Help

Available Tools:
1. rag_search - Search the vector database for relevant documents
2. rag_ingest_pdf - Load and ingest a PDF file into the vector database  
3. rag_get_stats - Get system statistics and status

Usage Examples:
- Search: Use rag_search with query "GPT-5 performance improvements"
- Ingest: Use rag_ingest_pdf with pdf_path "document.pdf"
- Stats: Use rag_get_stats to check system status

Environment Setup:
Make sure to set OPENAI_API_KEY, PGVECTOR_URL, and PGVECTOR_COLLECTION in your .env file.
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="rag_search",
            description="Search the RAG vector database for relevant documents based on semantic similarity",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant documents"
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 3, max: 10)",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rag_ingest_pdf",
            description="Load and ingest a PDF file into the vector database with configurable chunking",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "Path to the PDF file to ingest (relative to current directory)"
                    },
                    "chunk_size": {
                        "type": "integer",
                        "description": "Size of text chunks in characters (default: 1000)",
                        "default": 1000,
                        "minimum": 100,
                        "maximum": 5000
                    },
                    "chunk_overlap": {
                        "type": "integer",
                        "description": "Overlap between chunks in characters (default: 150)",
                        "default": 150,
                        "minimum": 0,
                        "maximum": 500
                    }
                },
                "required": ["pdf_path"]
            }
        ),
        Tool(
            name="rag_get_stats",
            description="Get comprehensive statistics and status information about the RAG system",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        if name == "rag_search":
            result = await rag_manager.search_documents(
                arguments.get("query", ""),
                arguments.get("k", 3)
            )
        elif name == "rag_ingest_pdf":
            result = await rag_manager.ingest_pdf(
                arguments.get("pdf_path", ""),
                arguments.get("chunk_size", 1000),
                arguments.get("chunk_overlap", 150)
            )
        elif name == "rag_get_stats":
            result = await rag_manager.get_system_stats()
        else:
            result = {
                "error": f"Unknown tool: {name}",
                "success": False,
                "available_tools": ["rag_search", "rag_ingest_pdf", "rag_get_stats"]
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        logger.error(f"Tool call failed: {str(e)}")
        error_result = {
            "error": f"Tool execution failed: {str(e)}",
            "success": False,
            "tool": name,
            "arguments": arguments
        }
        return [TextContent(
            type="text",
            text=json.dumps(error_result, indent=2)
        )]

async def main():
    """Main function to run the MCP server."""
    logger.info("Starting RAG Pipeline MCP Server...")
    
    # Check environment on startup
    startup_stats = await rag_manager.get_system_stats()
    logger.info(f"Startup status: {json.dumps(startup_stats, indent=2)}")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="rag-pipeline",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user")
    except Exception as e:
        logger.error(f"MCP Server error: {e}")
        sys.exit(1)
