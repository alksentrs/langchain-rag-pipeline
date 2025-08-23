#!/usr/bin/env python3
"""
Test script to verify MCP integration with the RAG pipeline.
This script tests the MCP server functionality without requiring external clients.
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

# Import the MCP server components
try:
    from mcp_server import rag_manager
except ImportError:
    print("❌ Failed to import MCP server components")
    sys.exit(1)

async def test_environment_setup():
    """Test if the environment is properly configured."""
    print("🔧 Testing environment setup...")
    
    stats = await rag_manager.get_system_stats()
    
    if stats.get("success"):
        env = stats.get("environment", {})
        all_good = all(status.startswith("✅") for status in env.values())
        
        if all_good:
            print("  ✅ Environment is properly configured")
            return True
        else:
            print("  ⚠️ Environment issues detected:")
            for key, status in env.items():
                print(f"    {key}: {status}")
            return False
    else:
        print(f"  ❌ Failed to get environment stats: {stats.get('error', 'Unknown error')}")
        return False

async def test_search_without_documents():
    """Test search functionality when no documents are ingested."""
    print("🔍 Testing search without documents...")
    
    result = await rag_manager.search_documents("test query", k=2)
    
    if result.get("success"):
        if result.get("results_count", 0) == 0:
            print("  ✅ Search works but returns no results (expected)")
            return True
        else:
            print(f"  ⚠️ Unexpected: Found {result.get('results_count')} results")
            return True
    else:
        print(f"  ❌ Search failed: {result.get('error', 'Unknown error')}")
        return False

async def test_pdf_ingestion():
    """Test PDF ingestion with a sample document."""
    print("📄 Testing PDF ingestion...")
    
    # Look for existing PDF files
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("  ⚠️ No PDF files found in current directory")
        print("  💡 To test ingestion, add a PDF file (e.g., gpt5.pdf) to the current directory")
        return False
    
    # Use the first PDF file found
    pdf_path = str(pdf_files[0])
    print(f"  📖 Testing with: {pdf_path}")
    
    result = await rag_manager.ingest_pdf(pdf_path, chunk_size=500, chunk_overlap=50)
    
    if result.get("success"):
        chunks = result.get("chunks_created", 0)
        print(f"  ✅ Successfully ingested {chunks} chunks from {os.path.basename(pdf_path)}")
        return True
    else:
        print(f"  ❌ Ingestion failed: {result.get('error', 'Unknown error')}")
        return False

async def test_search_with_documents():
    """Test search functionality after documents are ingested."""
    print("🔎 Testing search with ingested documents...")
    
    # Try a few different search queries
    test_queries = [
        "artificial intelligence",
        "machine learning",
        "performance",
        "evaluation",
        "results"
    ]
    
    successful_searches = 0
    
    for query in test_queries:
        result = await rag_manager.search_documents(query, k=2)
        
        if result.get("success"):
            results_count = result.get("results_count", 0)
            if results_count > 0:
                print(f"  ✅ Query '{query}': Found {results_count} results")
                successful_searches += 1
                
                # Show first result preview
                results = result.get("results", [])
                if results:
                    first_result = results[0]
                    content_preview = first_result.get("content", "")[:100]
                    score = first_result.get("score", 0)
                    print(f"    Top result (score: {score:.4f}): {content_preview}...")
            else:
                print(f"  ⚠️ Query '{query}': No results found")
        else:
            print(f"  ❌ Query '{query}' failed: {result.get('error', 'Unknown error')}")
    
    if successful_searches > 0:
        print(f"  ✅ {successful_searches}/{len(test_queries)} search queries successful")
        return True
    else:
        print("  ❌ No successful searches")
        return False

async def test_system_stats():
    """Test system statistics functionality."""
    print("📊 Testing system statistics...")
    
    stats = await rag_manager.get_system_stats()
    
    if stats.get("success"):
        print("  ✅ System stats retrieved successfully")
        
        # Check key fields
        required_fields = ["environment", "vector_store", "collection_name", "server_status"]
        missing_fields = [field for field in required_fields if field not in stats]
        
        if missing_fields:
            print(f"  ⚠️ Missing fields: {missing_fields}")
        else:
            print("  ✅ All required fields present")
        
        # Show ingestion info if available
        if "last_ingestion" in stats:
            ingestion = stats["last_ingestion"]
            print(f"  📄 Last ingestion: {ingestion.get('chunks_created', 0)} chunks from {os.path.basename(ingestion.get('pdf_path', 'unknown'))}")
        
        return True
    else:
        print(f"  ❌ Failed to get system stats: {stats.get('error', 'Unknown error')}")
        return False

async def run_comprehensive_test():
    """Run all tests in sequence."""
    print("🧪 MCP Integration Comprehensive Test")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Environment Setup
    result1 = await test_environment_setup()
    test_results.append(("Environment Setup", result1))
    
    if not result1:
        print("\n❌ Environment not properly configured. Please check your .env file.")
        print("Required variables: OPENAI_API_KEY, PGVECTOR_URL, PGVECTOR_COLLECTION")
        return
    
    print()
    
    # Test 2: Search without documents
    result2 = await test_search_without_documents()
    test_results.append(("Search (no documents)", result2))
    print()
    
    # Test 3: PDF Ingestion
    result3 = await test_pdf_ingestion()
    test_results.append(("PDF Ingestion", result3))
    print()
    
    # Test 4: Search with documents (only if ingestion succeeded)
    if result3:
        result4 = await test_search_with_documents()
        test_results.append(("Search (with documents)", result4))
        print()
    
    # Test 5: System Stats
    result5 = await test_system_stats()
    test_results.append(("System Statistics", result5))
    print()
    
    # Summary
    print("📋 Test Summary")
    print("-" * 30)
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP integration is working correctly.")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. Some minor issues may need attention.")
    else:
        print("❌ Several tests failed. Please check your configuration.")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("MCP Integration Test Script")
            print("Usage: python test_mcp_integration.py [--help]")
            print("\nThis script tests the MCP server integration with the RAG pipeline.")
            print("Make sure to have:")
            print("1. Environment variables configured (.env file)")
            print("2. PostgreSQL with pgvector running (docker-compose up -d)")
            print("3. Optional: PDF file in current directory for ingestion testing")
            return
    
    try:
        asyncio.run(run_comprehensive_test())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
