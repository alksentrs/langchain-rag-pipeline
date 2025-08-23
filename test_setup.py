#!/usr/bin/env python3
"""
Test script to verify the setup and dependencies.
Run this script to check if everything is configured correctly.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print(f"✅ LangChain: {langchain.__version__}")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import langchain_openai
        print(f"✅ LangChain OpenAI: {langchain_openai.__version__}")
    except ImportError as e:
        print(f"❌ LangChain OpenAI import failed: {e}")
        return False
    
    try:
        import langchain_postgres
        print(f"✅ LangChain Postgres: {langchain_postgres.__version__}")
    except ImportError as e:
        print(f"❌ LangChain Postgres import failed: {e}")
        return False
    
    try:
        import langchain_community
        print(f"✅ LangChain Community: {langchain_community.__version__}")
    except ImportError as e:
        print(f"❌ LangChain Community import failed: {e}")
        return False
    
    try:
        import langchain_text_splitters
        print(f"✅ LangChain Text Splitters: {langchain_text_splitters.__version__}")
    except ImportError as e:
        print(f"❌ LangChain Text Splitters import failed: {e}")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import psycopg2
        print(f"✅ psycopg2: {psycopg2.__version__}")
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
        return False
    
    try:
        import pypdf
        print(f"✅ PyPDF: {pypdf.__version__}")
    except ImportError as e:
        print(f"❌ PyPDF import failed: {e}")
        return False
    
    return True

def test_local_imports():
    """Test if local modules can be imported."""
    print("\n🔍 Testing local module imports...")
    
    try:
        from pdf_loader import load_and_split_pdf
        print("✅ pdf_loader module imported successfully")
    except ImportError as e:
        print(f"❌ pdf_loader import failed: {e}")
        return False
    
    try:
        from ingestion_pgvector import ingest_to_pgvector
        print("✅ ingestion_pgvector module imported successfully")
    except ImportError as e:
        print(f"❌ ingestion_pgvector import failed: {e}")
        return False
    
    try:
        from search_vector import search_vector_database
        print("✅ search_vector module imported successfully")
    except ImportError as e:
        print(f"❌ search_vector import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables."""
    print("\n🔍 Testing environment variables...")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ dotenv loaded successfully")
    except ImportError as e:
        print(f"❌ dotenv import failed: {e}")
        return False
    
    # Check required environment variables
    required_vars = ["OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: {'*' * len(os.getenv(var))} (hidden)")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    
    return True

def test_docker():
    """Test if Docker is running and PostgreSQL container is available."""
    print("\n🔍 Testing Docker setup...")
    
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
        else:
            print("❌ Docker not available")
            return False
    except Exception as e:
        print(f"❌ Docker test failed: {e}")
        return False
    
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose: {result.stdout.strip()}")
        else:
            print("❌ Docker Compose not available")
            return False
    except Exception as e:
        print(f"❌ Docker Compose test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 LangChain RAG Pipeline - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test local imports
    if not test_local_imports():
        all_passed = False
    
    # Test environment
    if not test_environment():
        all_passed = False
    
    # Test Docker
    if not test_docker():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start PostgreSQL: docker-compose up -d")
        print("2. Add a PDF file named 'gpt5.pdf'")
        print("3. Run: python main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Set up environment variables in .env file")
        print("3. Ensure Docker is running")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
