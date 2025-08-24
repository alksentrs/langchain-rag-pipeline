# 🤖 AI-Powered RAG Chat System

## Overview
This system combines vector similarity search with AI generation to provide intelligent, context-aware responses based on your ingested documents.

## 🚀 Features

### **Vector Search + AI Generation**
- **Vector Search**: Queries are vectorized and matched against your document database
- **Quality Filtering**: Only high-quality matches (similarity score ≥ 0.7) are used
- **AI Enhancement**: Relevant documents are sent to AI for intelligent response generation
- **Context-Aware**: AI responds based ONLY on the provided document context

### **Smart Quality Control**
- **Similarity Threshold**: Configurable threshold (default: 0.45) ensures only relevant results
- **Fallback Handling**: Clear messages when no relevant information is found
- **Score Transparency**: Shows relevance scores for transparency

## 📋 Requirements

### **Environment Variables**
Create a `.env` file with:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-3.5-turbo

# PostgreSQL with pgvector Configuration
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=langchain_pg_vector
```

### **Dependencies**
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### **Interactive Chat Mode**
```bash
python3 ai_rag_chat.py
```

**Commands:**
- `help` - Show usage information
- `quit` or `exit` - End the session
- Ask any question about your documents

### **Test Mode**
```bash
python3 test_rag_chat.py
```

## 🔍 How It Works

### **1. Query Processing**
- User enters a question
- Query is vectorized using OpenAI embeddings

### **2. Vector Search**
- Searches through your PGVector database
- Returns top 5 most similar document chunks
- Each result includes a similarity score

### **3. Quality Filtering**
- Filters results based on similarity threshold (0.7)
- Only high-quality matches proceed to AI generation

### **4. AI Response Generation**
- Creates a context-rich prompt with relevant documents
- Sends to OpenAI's chat model (GPT-3.5-turbo)
- AI generates response based on document context

### **5. Response Delivery**
- Returns intelligent, context-aware answer
- References specific document sections when possible

## 📊 Example Workflow

```
User: "O que acontece no caso de falecimento da autora?"

1. 🔍 Vector Search: Finds 5 relevant document chunks
2. ✅ Quality Filter: All chunks that meet threshold (score ≥ 0.45)
3. 🤖 AI Generation: Creates prompt with relevant context
4. 📝 Response: AI provides answer based on contract clauses
```

## ⚙️ Configuration

### **Similarity Threshold**
```python
self.similarity_threshold = 0.45  # Adjust in ai_rag_chat.py
```

### **Search Results**
```python
k=5  # Number of top results to retrieve
```

### **AI Model Settings**
```python
temperature=0.1      # Lower = more focused responses
max_tokens=1000     # Maximum response length
```

## 🎨 Customization

### **Prompt Engineering**
Modify the `create_ai_prompt()` method to customize:
- AI instructions
- Context formatting
- Response requirements

### **Quality Metrics**
Adjust the `filter_quality_results()` method for:
- Different similarity thresholds
- Custom filtering logic
- Score normalization

## 🔧 Troubleshooting

### **Common Issues**

1. **"No documents found"**
   - Check if documents are ingested
   - Verify database connection

2. **"No results met quality threshold"**
   - Lower similarity threshold
   - Check document relevance

3. **API errors**
   - Verify OpenAI API key
   - Check API quota/limits

### **Debug Mode**
Add debug prints in the code:
```python
print(f"Search results: {search_results}")
print(f"Quality results: {quality_results}")
```

## 🚀 Next Steps

### **Enhancements**
- **Multi-language support**
- **Conversation memory**
- **Document source tracking**
- **Response confidence scoring**

### **Integration**
- **Web interface**
- **API endpoints**
- **Slack/Discord bots**
- **Mobile apps**

## 📚 Files

- **`ai_rag_chat.py`** - Main chat system
- **`test_rag_chat.py`** - Test script
- **`RAG_CHAT_README.md`** - This documentation

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify environment variables
3. Test with simple queries first
4. Check API quotas and limits

---

**Enjoy your AI-powered document Q&A system! 🎉**
