# Deployment Guide for Render

## Prerequisites

1. GitHub account
2. Render account (free tier available at https://render.com)
3. API keys (OpenAI, Groq, or Gemini)

## Step-by-Step Deployment

### 1. Prepare Your Repository

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit: Multi-agent RAG chatbot"
   git push origin main
   ```

2. **Verify files are present**:
   - `requirements.txt`
   - `app.py`
   - `render.yaml`
   - `Dockerfile` (optional)
   - All Python modules
   - `data/` folder with documents

### 2. Create Render Service

#### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click **"Apply"**

#### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `multi-agent-rag-chatbot`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (or paid for better performance)

### 3. Configure Environment Variables

In Render dashboard, go to **Environment** tab and add:

```
OPENAI_API_KEY=sk-...your-key...
GROQ_API_KEY=gsk_...your-key...
GOOGLE_API_KEY=AI...your-key...
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

**Important**: Mark API keys as **Secret** to hide them in logs.

### 4. Deploy

1. Click **"Create Web Service"** or **"Deploy"**
2. Wait for build to complete (5-10 minutes first time)
3. Monitor logs for any errors
4. Once deployed, you'll get a URL like: `https://your-app.onrender.com`

### 5. Initialize Vector Stores

On first deployment, vector stores need to be created. This happens automatically when the app starts.

Monitor logs to see:
```
Initializing vector stores...
Loading documents from ./data/product...
Creating vector store for product with X chunks...
✓ product vector store created
...
✓ System initialized successfully!
```

### 6. Test Your Deployment

1. Open the Render URL in your browser
2. Try example queries:
   - "What products do you offer?"
   - "What is your return policy?"
   - "How do I troubleshoot technical issues?"

## Troubleshooting

### Build Fails

**Error**: `No module named 'X'`
- **Solution**: Add missing package to `requirements.txt`

**Error**: `Python version mismatch`
- **Solution**: Add to `render.yaml`:
  ```yaml
  envVars:
    - key: PYTHON_VERSION
      value: 3.11.0
  ```

### Runtime Errors

**Error**: `OPENAI_API_KEY not found`
- **Solution**: Add API key in Environment Variables

**Error**: `Port already in use`
- **Solution**: Render automatically assigns port. Ensure `app.py` uses:
  ```python
  interface.launch(server_name="0.0.0.0", server_port=7860)
  ```

**Error**: `ChromaDB initialization failed`
- **Solution**: Check logs. May need to increase memory (upgrade plan)

### Performance Issues

**Slow responses**:
- Free tier has limited resources
- Consider upgrading to paid plan
- Optimize chunk sizes in `vector_store.py`

**Timeout errors**:
- Increase timeout in Render settings
- Use faster model (e.g., `gpt-4o-mini` instead of `gpt-4`)

## Monitoring

### View Logs

1. Go to Render dashboard
2. Select your service
3. Click **"Logs"** tab
4. Monitor real-time logs

### Check Health

Render provides:
- **Health checks**: Automatic
- **Metrics**: CPU, Memory usage
- **Uptime**: Service availability

## Updating Your Deployment

### Automatic Deploys

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update feature X"
   git push origin main
   ```

2. Render auto-deploys on push (if enabled)

### Manual Deploy

1. Go to Render dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## Cost Optimization

### Free Tier Limits

- 750 hours/month free
- Spins down after 15 min inactivity
- Cold start: ~30 seconds

### Tips

1. **Use efficient models**: `gpt-4o-mini` is cheaper than `gpt-4`
2. **Cache embeddings**: Vector stores persist between deploys
3. **Limit context**: Reduce `k` in similarity search
4. **Monitor usage**: Check OpenAI dashboard for API costs

## Security Best Practices

1. **Never commit API keys**: Use environment variables
2. **Use secrets**: Mark sensitive vars as Secret in Render
3. **Restrict access**: Use Render's authentication if needed
4. **Monitor logs**: Check for suspicious activity
5. **Update dependencies**: Keep packages up to date

## Scaling

### Horizontal Scaling

Render supports multiple instances:
1. Upgrade to paid plan
2. Enable auto-scaling
3. Configure min/max instances

### Vertical Scaling

Upgrade instance size:
- **Free**: 512MB RAM
- **Starter**: 1GB RAM
- **Standard**: 2GB+ RAM

## Custom Domain

1. Go to **Settings** → **Custom Domain**
2. Add your domain
3. Update DNS records as instructed
4. Enable HTTPS (automatic with Render)

## Backup and Recovery

### Backup Vector Stores

```bash
# Download from Render
render ssh
tar -czf chroma_backup.tar.gz chroma_db/
# Download to local
```

### Restore

```bash
# Upload to Render
render ssh
tar -xzf chroma_backup.tar.gz
```

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: Open issue in your repo

---

## Quick Reference

### Render Dashboard URLs

- Dashboard: https://dashboard.render.com
- Logs: `https://dashboard.render.com/web/[service-id]/logs`
- Environment: `https://dashboard.render.com/web/[service-id]/env`

### Useful Commands

```bash
# View logs
render logs

# SSH into service
render ssh

# Restart service
render restart

# Check status
render status
```

---

**Deployment Complete!** 🎉

Your multi-agent RAG chatbot is now live and accessible worldwide.
