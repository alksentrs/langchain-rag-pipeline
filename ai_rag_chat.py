#!/usr/bin/env python3
"""
AI-Powered RAG Chat System
Combines vector search with AI generation for intelligent document Q&A
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sys

class RAGChatSystem:
    def __init__(self):
        """Initialize the RAG chat system with database and AI components."""
        load_dotenv()
        
        # Check required environment variables
        required_vars = ["OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
        for var in required_vars:
            if not os.getenv(var):
                raise RuntimeError(f"Missing required environment variable: {var}")
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
        )
        
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
        
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo"),
            temperature=0.1,
            max_tokens=1000
        )
        
        # Set similarity threshold for quality control
        self.similarity_threshold = 0.45
        
    def search_documents(self, query, k=5):
        """
        Perform vector similarity search on the database.
        
        Args:
            query: User's search query
            k: Number of top results to return
            
        Returns:
            List of (document, score) tuples
        """
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error during vector search: {e}")
            return []
    
    def filter_quality_results(self, results):
        """
        Filter results based on similarity score threshold.
        
        Args:
            results: List of (document, score) tuples
            
        Returns:
            Filtered list of high-quality results
        """
        quality_results = []
        
        for doc, score in results:
            # Convert similarity score to distance (lower is better)
            distance = 1 - score
            if distance <= (1 - self.similarity_threshold):
                quality_results.append((doc, score))
        
        return quality_results
    
    def create_ai_prompt(self, query, relevant_docs):
        """
        Create a prompt for the AI based on the query and relevant documents.
        
        Args:
            query: User's original question
            relevant_docs: List of relevant documents with scores
            
        Returns:
            Formatted prompt string
        """
        context_parts = []
        
        for i, (doc, score) in enumerate(relevant_docs, 1):
            context_parts.append(f"""
Document {i} (Relevance Score: {score:.3f}):
Content: {doc.page_content}
Metadata: Page {doc.metadata.get('page', 'N/A')}, Source: {doc.metadata.get('source', 'N/A')}
---""")
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are a helpful AI assistant that answers questions based on the provided document context.

User Question: {query}

Relevant Document Context:
{context}

Instructions:
1. Answer the user's question based ONLY on the information provided in the documents above
2. If the documents don't contain enough information to answer the question, say "I don't have enough information to answer this question based on the available documents."
3. If the documents contain the answer, provide a clear, accurate response
4. Reference specific parts of the documents when possible
5. Keep your response concise but informative
6. Respond in the same language as the user's question

Your Answer:"""
        
        return prompt
    
    def get_ai_response(self, prompt):
        """
        Get AI response using the OpenAI API.
        
        Args:
            prompt: Formatted prompt for the AI
            
        Returns:
            AI-generated response
        """
        try:
            # Create a simple prompt template
            prompt_template = ChatPromptTemplate.from_template("{prompt}")
            
            # Create the chain
            chain = prompt_template | self.llm | StrOutputParser()
            
            # Get response
            response = chain.invoke({"prompt": prompt})
            return response
            
        except Exception as e:
            return f"Error getting AI response: {e}"
    
    def clean_query(self, query: str) -> str:
        """
        Clean and normalize user query for better search results.
        
        Args:
            query: Raw user query
            
        Returns:
            Cleaned and normalized query
        """
        import re
        
        # Store original for comparison
        original = query
        
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query)
        
        # Normalize punctuation spacing
        query = re.sub(r'\s+([.!?])', r'\1', query)
        query = re.sub(r'([.!?])\s*', r'\1 ', query)
        
        # Remove leading/trailing whitespace
        query = query.strip()
        
        # Remove common noise characters (optional)
        # query = re.sub(r'[^\w\s.!?]', '', query)
        
        # Convert to lowercase for better matching (optional)
        # query = query.lower()
        
        # Log if query was modified
        if original != query:
            print(f"🧹 Query cleaned: '{original}' → '{query}'")
        
        return query
    
    def analyze_query(self, original_query: str, cleaned_query: str) -> dict:
        """
        Analyze the query preprocessing results.
        
        Args:
            original_query: User's original query
            cleaned_query: Processed query
            
        Returns:
            Analysis results
        """
        import re
        
        analysis = {
            'original_length': len(original_query),
            'cleaned_length': len(cleaned_query),
            'whitespace_reduction': original_query.count(' ') - cleaned_query.count(' '),
            'was_modified': original_query != cleaned_query,
            'modification_type': []
        }
        
        if original_query != cleaned_query:
            if len(original_query) != len(cleaned_query):
                analysis['modification_type'].append('length_changed')
            if original_query.strip() != original_query:
                analysis['modification_type'].append('whitespace_trimmed')
            if re.sub(r'\s+', ' ', original_query) != original_query:
                analysis['modification_type'].append('whitespace_normalized')
        
        return analysis
    
    def chat(self, query):
        """
        Main chat method that combines vector search with AI generation.
        
        Args:
            query: User's question
            
        Returns:
            AI-generated response based on relevant documents
        """
        # Clean and normalize the query
        original_query = query
        cleaned_query = self.clean_query(query)
        
        # Analyze query preprocessing
        query_analysis = self.analyze_query(original_query, cleaned_query)
        
        if query_analysis['was_modified']:
            print(f"🔍 Original query: '{original_query}'")
            print(f"🧹 Cleaned query: '{cleaned_query}'")
            print(f"📊 Query analysis: {query_analysis['modification_type']}")
        
        print(f"\n🔍 Searching for: '{cleaned_query}'")
        print("=" * 60)
        
        # Step 1: Vector search with cleaned query
        search_results = self.search_documents(cleaned_query, k=5)
        
        if not search_results:
            return "❌ No documents found in the database. Please check if documents have been ingested."
        
        print(f"📚 Found {len(search_results)} search results")
        
        # DEBUG: Print all search results with scores
        print("\n🔍 DEBUG: All Search Results:")
        print("=" * 60)
        for i, (doc, score) in enumerate(search_results, 1):
            print(f"\n--- Result {i} (Score: {score:.4f}) ---")
            print(f"Content Preview: {doc.page_content[:200]}...")
            print(f"Metadata: Page {doc.metadata.get('page', 'N/A')}, Source: {doc.metadata.get('source', 'N/A')}")
        
        # Step 2: Filter by quality
        quality_results = self.filter_quality_results(search_results)
        
        print(f"\n✅ {len(quality_results)} results met quality threshold (≥{self.similarity_threshold})")
        
        # DEBUG: Print quality-filtered results
        if quality_results:
            print("\n🔍 DEBUG: Quality-Filtered Results:")
            print("=" * 60)
            for i, (doc, score) in enumerate(quality_results, 1):
                print(f"\n--- Quality Result {i} (Score: {score:.4f}) ---")
                print(f"Content Preview: {doc.page_content[:200]}...")
                print(f"Metadata: Page {doc.metadata.get('page', 'N/A')}, Source: {doc.metadata.get('source', 'N/A')}")
        else:
            print("\n❌ DEBUG: No results passed quality threshold")
            print(f"Threshold: {self.similarity_threshold}")
            print("All scores were below the threshold")
            return f"❌ No documents met the quality threshold (similarity score >= {self.similarity_threshold}). The available information may not be relevant enough to answer your question accurately."
        
        # Step 3: Create AI prompt
        prompt = self.create_ai_prompt(query, quality_results)
        
        # Step 4: Get AI response
        print("🤖 Generating AI response...")
        ai_response = self.get_ai_response(prompt)
        
        return ai_response

def main():
    """Main interactive chat loop."""
    print("🤖 AI-Powered RAG Chat System")
    print("=" * 40)
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'help' for usage information")
    print()
    
    try:
        # Initialize the RAG system
        rag_system = RAGChatSystem()
        print("✅ RAG system initialized successfully!")
        print()
        
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        return
    
    # Interactive chat loop
    while True:
        try:
            # Get user input
            user_query = input("\n💬 Your question: ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thanks for using the RAG Chat System.")
                break
            
            # Check for help command
            if user_query.lower() == 'help':
                print("\n📖 Usage Information:")
                print("- Ask questions about your ingested documents")
                print("- The system will search through your vector database")
                print("- Only high-quality matches are used for AI generation")
                print("- Type 'quit' or 'exit' to end the session")
                continue
            
            # Skip empty queries
            if not user_query:
                continue
            
            # Process the query
            response = rag_system.chat(user_query)
            
            # Display the response
            print("\n🤖 AI Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the RAG Chat System.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    main()
