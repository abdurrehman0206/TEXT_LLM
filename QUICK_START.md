# Quick Start - Docker Testing

## 🚀 Quick Commands

### 1. Build Docker Image
```bash
docker build -t paraphrase-api .
```

### 2. Run Container (Windows PowerShell)
```powershell
docker run -d --name paraphrase-api-container -p 8000:8000 -v "${PWD}/llama-2-13b.Q4_K_M.gguf:/app/models/llama-2-13b.Q4_K_M.gguf:ro" -e MODEL_PATH=/app/models/llama-2-13b.Q4_K_M.gguf paraphrase-api
```

### 3. Check Logs (Wait for "Model loaded successfully!")
```bash
docker logs -f paraphrase-api-container
```

### 4. Test API (in new terminal)
```bash
# Option A: Use the test script
python test_api.py

# Option B: Manual test
curl http://localhost:8000/health
```

### 5. Open API Docs in Browser
```
http://localhost:8000/docs
```

### 6. Stop Container
```bash
docker stop paraphrase-api-container
```

---

## 📋 Full Step-by-Step Guide

See `DOCKER_TESTING.md` for detailed instructions.

