#!/usr/bin/env python3
"""
Example MCP client that demonstrates how to interact with the RAG MCP server.
This shows how external applications can use the RAG pipeline via MCP.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

class MCPClient:
    """Simple MCP client for testing the RAG server."""
    
    def __init__(self, server_command: List[str] = None):
        """Initialize the MCP client.
        
        Args:
            server_command: Command to start the MCP server (default: ['python', 'mcp_server.py'])
        """
        self.server_command = server_command or ['python', 'mcp_server.py']
        self.process = None
    
    async def start_server(self):
        """Start the MCP server process."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            print("✅ MCP Server started")
            return True
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False
    
    async def send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a request to the MCP server."""
        if not self.process:
            print("❌ MCP server not started")
            return None
        
        try:
            # Send request
            request_json = json.dumps(request) + '\n'
            self.process.stdin.write(request_json.encode())
            await self.process.stdin.drain()
            
            # Read response
            response_line = await self.process.stdout.readline()
            if response_line:
                return json.loads(response_line.decode().strip())
            return None
        except Exception as e:
            print(f"❌ Failed to communicate with server: {e}")
            return None
    
    async def list_tools(self) -> Optional[List[Dict[str, Any]]]:
        """List available tools from the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = await self.send_request(request)
        if response and "result" in response:
            return response["result"]["tools"]
        return None
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a tool on the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = await self.send_request(request)
        if response and "result" in response:
            return response["result"]
        return response
    
    async def list_resources(self) -> Optional[List[Dict[str, Any]]]:
        """List available resources from the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        response = await self.send_request(request)
        if response and "result" in response:
            return response["result"]["resources"]
        return None
    
    async def read_resource(self, uri: str) -> Optional[str]:
        """Read a resource from the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        }
        
        response = await self.send_request(request)
        if response and "result" in response:
            return response["result"]["contents"][0]["text"]
        return None
    
    async def stop_server(self):
        """Stop the MCP server process."""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("✅ MCP Server stopped")

async def demo_mcp_interaction():
    """Demonstrate MCP client interactions with the RAG server."""
    print("🚀 MCP RAG Client Demo")
    print("=" * 50)
    
    client = MCPClient()
    
    try:
        # Start the server
        if not await client.start_server():
            return
        
        # Wait a moment for server to initialize
        await asyncio.sleep(2)
        
        # Test 1: List available tools
        print("\n📋 Listing available tools...")
        tools = await client.list_tools()
        if tools:
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        else:
            print("  ❌ Failed to list tools")
        
        # Test 2: Get system stats
        print("\n📊 Getting system statistics...")
        stats_result = await client.call_tool("rag_get_stats", {})
        if stats_result:
            print("  System Status:")
            if "content" in stats_result:
                stats_data = json.loads(stats_result["content"][0]["text"])
                print(f"    Environment: {stats_data.get('environment', {})}")
                print(f"    Vector Store: {stats_data.get('vector_store', 'Unknown')}")
                print(f"    Collection: {stats_data.get('collection_name', 'Unknown')}")
        
        # Test 3: List resources
        print("\n📁 Listing available resources...")
        resources = await client.list_resources()
        if resources:
            for resource in resources:
                print(f"  - {resource['uri']}: {resource['name']}")
        
        # Test 4: Read help resource
        print("\n📖 Reading help resource...")
        help_content = await client.read_resource("rag://help")
        if help_content:
            print("  Help Content (first 200 chars):")
            print(f"  {help_content[:200]}...")
        
        # Test 5: Try a search (this might fail if no documents are ingested)
        print("\n🔍 Testing search functionality...")
        search_result = await client.call_tool("rag_search", {
            "query": "test search query",
            "k": 2
        })
        if search_result:
            if "content" in search_result:
                search_data = json.loads(search_result["content"][0]["text"])
                if search_data.get("success"):
                    print(f"  ✅ Search successful: {search_data.get('results_count', 0)} results")
                else:
                    print(f"  ⚠️ Search failed: {search_data.get('error', 'Unknown error')}")
        
        print("\n🎉 Demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        await client.stop_server()

async def interactive_demo():
    """Interactive demo allowing user input."""
    print("🎮 Interactive MCP RAG Demo")
    print("=" * 50)
    print("Commands:")
    print("  search <query>     - Search the knowledge base")
    print("  ingest <pdf_path>  - Ingest a PDF file")
    print("  stats              - Show system statistics")
    print("  help               - Show help")
    print("  quit               - Exit")
    print()
    
    client = MCPClient()
    
    try:
        if not await client.start_server():
            return
        
        await asyncio.sleep(2)  # Wait for server to initialize
        
        while True:
            try:
                user_input = input("mcp-rag> ").strip()
                
                if not user_input:
                    continue
                
                if user_input == "quit":
                    break
                
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                
                if command == "search":
                    if len(parts) < 2:
                        print("Usage: search <query>")
                        continue
                    
                    query = parts[1]
                    result = await client.call_tool("rag_search", {"query": query, "k": 3})
                    
                    if result and "content" in result:
                        data = json.loads(result["content"][0]["text"])
                        if data.get("success"):
                            print(f"Found {data.get('results_count', 0)} results:")
                            for res in data.get("results", []):
                                print(f"  [{res['rank']}] Score: {res['score']:.4f}")
                                print(f"      {res['content'][:200]}...")
                                print()
                        else:
                            print(f"Search failed: {data.get('error', 'Unknown error')}")
                
                elif command == "ingest":
                    if len(parts) < 2:
                        print("Usage: ingest <pdf_path>")
                        continue
                    
                    pdf_path = parts[1]
                    result = await client.call_tool("rag_ingest_pdf", {"pdf_path": pdf_path})
                    
                    if result and "content" in result:
                        data = json.loads(result["content"][0]["text"])
                        if data.get("success"):
                            print(f"✅ Ingested {data.get('chunks_created', 0)} chunks from {pdf_path}")
                        else:
                            print(f"❌ Ingestion failed: {data.get('error', 'Unknown error')}")
                
                elif command == "stats":
                    result = await client.call_tool("rag_get_stats", {})
                    
                    if result and "content" in result:
                        data = json.loads(result["content"][0]["text"])
                        print("System Statistics:")
                        print(json.dumps(data, indent=2))
                
                elif command == "help":
                    help_content = await client.read_resource("rag://help")
                    if help_content:
                        print(help_content)
                
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
    finally:
        await client.stop_server()

def main():
    """Main function with command line argument handling."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_demo())
    else:
        asyncio.run(demo_mcp_interaction())

if __name__ == "__main__":
    main()
