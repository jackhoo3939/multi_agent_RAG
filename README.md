# Multi-Agent RAG Chatbot

A sophisticated multi-agent chatbot system with Retrieval-Augmented Generation (RAG), intelligent routing, and custom tools. Built with LangChain, LangGraph, ChromaDB, and Gradio.

## 🌟 Features

- **3 Specialized Agents**: Product, Policy, and Tech Support agents with domain expertise
- **Intelligent Router**: Automatically routes queries to the appropriate agent using LangGraph
- **RAG Knowledge Base**: ChromaDB vector store with embeddings from domain-specific documents
- **Custom Tools**:
  - 🔍 DuckDuckGo Search for current information
  - 💰 Salary Predictor using ML model
- **Web Interface**: Interactive Gradio UI for easy testing
- **Cloud Deployment**: Ready to deploy on Render

## 📁 Project Structure

```
multi_agent_RAG/
├── data/                      # Knowledge base documents
│   ├── product/              # Product information
│   ├── policy/               # Company policies
│   └── tech/                 # Technical support docs
├── agents.py                 # Agent definitions with RAG
├── router.py                 # LangGraph routing system
├── tools.py                  # Custom tools (DuckDuckGo, Salary)
├── vector_store.py           # ChromaDB setup and management
├── app.py                    # Gradio web interface
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── render.yaml               # Render deployment config
├── setup.sh                  # Local setup script
├── .env.example              # Environment variables template
└── salary_model.joblib       # Pre-trained salary prediction model
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key (or Groq/Gemini)

### Local Setup

1. **Clone and navigate to the project**:
   ```bash
   cd multi_agent_RAG
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   ```

3. **Run setup script** (Linux/Mac):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python vector_store.py
   ```

4. **Launch the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** to `http://localhost:7860`

## 🎯 Usage Examples

### Product Questions
- "What products do you offer?"
- "Tell me about your laptop specifications"
- "Compare product X and Y"

### Policy Questions
- "What is your return policy?"
- "How long is the warranty?"
- "What are your delivery options?"

### Technical Support
- "How do I reset my password?"
- "Troubleshoot connection issues"
- "Installation guide for product X"

### Using Tools
- "Search for latest AI trends" (uses DuckDuckGo)
- "Predict salary for software engineer with 5 years experience" (uses Salary Predictor)

## 🏗️ Architecture

### Agent System
```
User Query → Router (LangGraph) → Agent Selection → RAG Retrieval → LLM Response
                                      ↓
                              [Product | Policy | Tech]
                                      ↓
                              ChromaDB Vector Store
```

### Components

1. **Router** (`router.py`): LangGraph-based state machine that classifies queries
2. **Agents** (`agents.py`): Specialized agents with RAG capabilities
3. **Vector Store** (`vector_store.py`): ChromaDB for document embeddings
4. **Tools** (`tools.py`): Custom tools for extended functionality
5. **UI** (`app.py`): Gradio interface for user interaction

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `GROQ_API_KEY` | Groq API key | Optional |
| `GOOGLE_API_KEY` | Google Gemini key | Optional |
| `OPENAI_MODEL` | LLM model | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |

### Adding New Documents

1. Add `.txt` files to appropriate folder in `data/`:
   - `data/product/` for product info
   - `data/policy/` for policies
   - `data/tech/` for technical docs

2. Reinitialize vector stores:
   ```bash
   python vector_store.py
   ```

## 🌐 Deployment on Render

### Option 1: Using render.yaml

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-detect `render.yaml`
4. Add environment variables in Render dashboard
5. Deploy!

### Option 2: Manual Setup

1. Create new Web Service on Render
2. Connect your repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3.11
4. Add environment variables
5. Deploy

### Environment Variables on Render

Add these in the Render dashboard:
- `OPENAI_API_KEY`
- `GROQ_API_KEY` (optional)
- `GOOGLE_API_KEY` (optional)

## 🛠️ Development

### Testing Individual Components

**Test Vector Store**:
```bash
python vector_store.py
```

**Test Router**:
```bash
python router.py
```

**Test Tools**:
```python
from tools import get_tools
tools = get_tools()
# Test DuckDuckGo
tools[0]._run("latest AI news")
# Test Salary Predictor
tools[1]._run(5, 2, "Software Engineer")
```

### Adding New Agents

1. Add documents to `data/new_agent/`
2. Update `vector_store.py` to include new domain
3. Add agent definition in `agents.py`
4. Update router classification in `router.py`

## 📊 System Requirements

- **Memory**: 2GB+ RAM
- **Storage**: 500MB+ (for vector stores)
- **Network**: Internet connection for API calls

## 🔒 Security Notes

- `.env` file is gitignored to protect API keys
- Never commit API keys to version control
- Use environment variables for sensitive data
- Render encrypts environment variables

## 🐛 Troubleshooting

### Vector Store Issues
```bash
# Delete and recreate
rm -rf chroma_db/
python vector_store.py
```

### API Key Errors
- Verify keys in `.env` file
- Check key has sufficient credits
- Ensure correct key format

### Port Already in Use
```bash
# Change port in app.py
interface.launch(server_port=7861)
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using LangChain, LangGraph, ChromaDB, and Gradio
