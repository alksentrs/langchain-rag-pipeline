#!/usr/bin/env python3
"""
Startup script for the MCP RAG server.
This script provides an easy way to start the MCP server with proper logging and error handling.
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

def setup_logging(debug: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('mcp_server.log')
        ]
    )

def check_environment():
    """Check if the environment is properly configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    
    print("✅ Environment variables are properly configured")
    return True

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import mcp
        import langchain
        import langchain_openai
        import langchain_postgres
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if the database is accessible."""
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try to connect to the database
        conn_string = os.getenv("PGVECTOR_URL")
        if not conn_string:
            print("❌ PGVECTOR_URL not configured")
            return False
        
        conn = psycopg2.connect(conn_string)
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running: docker-compose up -d")
        return False

async def start_server(debug: bool = False):
    """Start the MCP server."""
    setup_logging(debug)
    logger = logging.getLogger(__name__)
    
    print("🚀 Starting MCP RAG Server")
    print("=" * 50)
    
    # Pre-flight checks
    if not check_environment():
        return False
    
    if not check_dependencies():
        return False
    
    if not check_database():
        return False
    
    print("✅ All pre-flight checks passed")
    print("\n🔄 Starting MCP server...")
    
    try:
        # Import and run the MCP server
        from mcp_server import main
        await main()
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user")
        print("\n👋 MCP Server stopped")
        return True
    except Exception as e:
        logger.error(f"MCP Server error: {e}")
        print(f"\n❌ MCP Server failed: {e}")
        return False

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Start the MCP RAG Server")
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    parser.add_argument(
        "--check-only", 
        action="store_true", 
        help="Only run pre-flight checks without starting server"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="MCP RAG Server 1.0.0"
    )
    
    args = parser.parse_args()
    
    if args.check_only:
        print("🔍 Running pre-flight checks...")
        env_ok = check_environment()
        deps_ok = check_dependencies()
        db_ok = check_database()
        
        if all([env_ok, deps_ok, db_ok]):
            print("\n🎉 All checks passed! Ready to start the server.")
            return 0
        else:
            print("\n❌ Some checks failed. Please fix the issues above.")
            return 1
    
    try:
        success = asyncio.run(start_server(args.debug))
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
