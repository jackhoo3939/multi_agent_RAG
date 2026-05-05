# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up API Keys

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor and add your API keys:
   ```
   OPENAI_API_KEY=sk-proj-...your-key...
   GROQ_API_KEY=gsk_...your-key...
   GOOGLE_API_KEY=AI...your-key...
   ```

   **Where to get API keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Groq: https://console.groq.com/keys
   - Google Gemini: https://makersuite.google.com/app/apikey

3. Save the file. Your keys are now secure (`.env` is gitignored).

### Step 2: Install Dependencies

**Option A: Using setup script (Linux/Mac)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option B: Manual installation**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Initialize vector stores
python vector_store.py
```

### Step 3: Run the Application

```bash
python app.py
```

You should see:
```
Initializing system...
Loading documents from ./data/product...
✓ product vector store created
...
✓ System initialized successfully!
Running on local URL:  http://127.0.0.1:7860
```

### Step 4: Open in Browser

Open http://localhost:7860 in your web browser.

### Step 5: Try It Out!

Ask questions like:
- "What products do you offer?"
- "What is your return policy?"
- "How do I troubleshoot technical issues?"
- "Search for latest AI trends"
- "Predict salary for 5 years experience as software engineer"

---

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_system.py
```

This will test:
- ✓ Environment variables
- ✓ Vector store initialization
- ✓ Custom tools (DuckDuckGo, Salary Predictor)
- ✓ Agent initialization
- ✓ Router functionality
- ✓ Full system integration

---

## 🐛 Common Issues

### "OPENAI_API_KEY not found"
- Make sure you created `.env` file (not `.env.example`)
- Check that API key is correctly formatted
- Restart the application after adding keys

### "No module named 'X'"
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "ChromaDB initialization failed"
- Run: `python vector_store.py`
- Check that `data/` folder exists with documents

### Port 7860 already in use
- Change port in `app.py`:
  ```python
  interface.launch(server_port=7861)
  ```

---

## 📚 Next Steps

1. **Add your own documents**: Place `.txt` files in `data/product/`, `data/policy/`, or `data/tech/`
2. **Customize agents**: Edit prompts in `agents.py`
3. **Add new tools**: Create tools in `tools.py`
4. **Deploy to cloud**: Follow `DEPLOYMENT.md`

---

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- Check `DEPLOYMENT.md` for deployment guide
- Open an issue on GitHub

---

**That's it! You're ready to go.** 🎉
