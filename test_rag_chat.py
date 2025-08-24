#!/usr/bin/env python3
"""
Test script for the RAG Chat System
"""

from ai_rag_chat import RAGChatSystem

def test_single_query():
    """Test a single query to demonstrate the system."""
    try:
        # Initialize the system
        print("🚀 Initializing RAG Chat System...")
        rag_system = RAGChatSystem()
        print("✅ System initialized successfully!")
        
        # Test query
        test_query = "O que acontece no caso de falecimento da autora?"
        print(f"\n🔍 Testing query: '{test_query}'")
        
        # Get response
        response = rag_system.chat(test_query)
        
        # Display response
        print("\n🤖 AI Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_query()
