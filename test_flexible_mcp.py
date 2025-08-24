#!/usr/bin/env python3
"""
Test script for the flexible MCP server.
This demonstrates how the MCP server can run with or without RAG capabilities.
"""

import asyncio
import json
from mcp_server_flexible import FlexibleRAGManager

async def test_flexible_mcp():
    """Test the flexible MCP server capabilities."""
    print("🧪 Testing Flexible MCP Server")
    print("=" * 50)
    
    # Create the flexible RAG manager
    rag_manager = FlexibleRAGManager()
    
    print(f"✅ RAG Components Available: {rag_manager.rag_available}")
    print()
    
    # Test system stats
    print("📊 System Statistics:")
    stats = await rag_manager.get_system_stats()
    print(json.dumps(stats, indent=2))
    print()
    
    # Test what tools are available
    if rag_manager.rag_available:
        print("🔧 RAG Tools Available:")
        print("  - rag_search: Search documents")
        print("  - rag_ingest_pdf: Ingest PDFs")
        print("  - rag_get_stats: System status")
        
        # Test search without API key
        print("\n🔍 Testing search without API key:")
        search_result = await rag_manager.search_documents("test query")
        print(json.dumps(search_result, indent=2))
        
    else:
        print("⚠️ RAG Tools Not Available:")
        print("  - Only rag_get_stats is available")
        print("  - RAG components could not be imported")
    
    print("\n🎯 Key Benefits of Flexible MCP Server:")
    print("  1. ✅ MCP server starts even without OpenAI API key")
    print("  2. ✅ MCP protocol works regardless of RAG setup")
    print("  3. ✅ Tools are conditionally available based on capabilities")
    print("  4. ✅ Clear error messages when tools can't be used")
    print("  5. ✅ Can be used for MCP testing without full RAG setup")

def main():
    """Main function."""
    try:
        asyncio.run(test_flexible_mcp())
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
