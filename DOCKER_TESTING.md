# Docker Testing Guide - Step by Step

## Prerequisites
- Docker installed and running
- Model file `llama-2-13b.Q4_K_M.gguf` in your project directory

## Step 1: Verify Your Files

Make sure you have these files in your project directory:
- `main.py`
- `paraphrase_service.py`
- `requirements.txt`
- `Dockerfile`
- `llama-2-13b.Q4_K_M.gguf` (the model file)

## Step 2: Build the Docker Image

Open your terminal/PowerShell in the project directory and run:

```bash
docker build -t paraphrase-api .
```

This will:
- Download the Python base image
- Install system dependencies
- Install Python packages
- Copy your application files
- Set up the container

**Expected output:** You should see the build process and it should complete with "Successfully tagged paraphrase-api:latest"

## Step 3: Verify the Image was Created

Check that the image exists:

```bash
docker images | grep paraphrase-api
```

You should see your image listed.

## Step 4: Run the Docker Container

Run the container with the model file mounted:

```bash
docker run -d \
  --name paraphrase-api-container \
  -p 8000:8000 \
  -v "${PWD}/llama-2-13b.Q4_K_M.gguf:/app/models/llama-2-13b.Q4_K_M.gguf:ro" \
  -e MODEL_PATH=/app/models/llama-2-13b.Q4_K_M.gguf \
  paraphrase-api
```

**For Windows PowerShell, use:**
```powershell
docker run -d `
  --name paraphrase-api-container `
  -p 8000:8000 `
  -v "${PWD}/llama-2-13b.Q4_K_M.gguf:/app/models/llama-2-13b.Q4_K_M.gguf:ro" `
  -e MODEL_PATH=/app/models/llama-2-13b.Q4_K_M.gguf `
  paraphrase-api
```

**Note:** The model loading will take some time (1-2 minutes). The container is running in detached mode (`-d`).

## Step 5: Check Container Status

Check if the container is running:

```bash
docker ps
```

You should see `paraphrase-api-container` in the list.

## Step 6: View Container Logs

Watch the logs to see when the model finishes loading:

```bash
docker logs -f paraphrase-api-container
```

**What to look for:**
- "Loading model from /app/models/llama-2-13b.Q4_K_M.gguf..."
- "Model loaded successfully!"
- "Application startup complete"
- "Uvicorn running on http://0.0.0.0:8000"

Press `Ctrl+C` to stop following logs (container keeps running).

## Step 7: Test the Health Endpoint

Once you see "Model loaded successfully!" in the logs, test the health endpoint:

```bash
curl http://localhost:8000/health
```

**Or in PowerShell:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content
```

**Expected response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Step 8: Test the Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected response:**
```json
{
  "message": "Article Paraphrasing API",
  "status": "running",
  "model_loaded": true
}
```

## Step 9: Test the Paraphrase Endpoint

Test with a sample article:

```bash
curl -X POST "http://localhost:8000/paraphrase" \
  -H "Content-Type: application/json" \
  -d "{\"article\": \"The Minister of Livestock and Rural Development of Somaliland, Omar Shucayb Mohamed, stated that the country's economy heavily relies on livestocks. He said: 'When looking at the national economy, 70% of our revenue comes from livestock.'\", \"max_tokens\": 500}"
```

**Or in PowerShell:**
```powershell
$body = @{
    article = "The Minister of Livestock and Rural Development of Somaliland, Omar Shucayb Mohamed, stated that the country's economy heavily relies on livestocks. He said: 'When looking at the national economy, 70% of our revenue comes from livestock.'"
    max_tokens = 500
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/paraphrase" -Method Post -Body $body -ContentType "application/json"
```

**Expected response:**
```json
{
  "original_article": "...",
  "paraphrased_article": "...",
  "statistics": {
    "original_word_count": 35,
    "paraphrased_word_count": 38,
    "length_match_percentage": 108.57,
    "inference_time_seconds": 15.23,
    "tokens_per_second": 2.49
  }
}
```

## Step 10: Access API Documentation

Open your browser and visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test the API directly from the Swagger UI interface!

## Step 11: Stop the Container

When you're done testing:

```bash
docker stop paraphrase-api-container
```

## Step 12: Remove the Container (Optional)

To remove the container:

```bash
docker rm paraphrase-api-container
```

## Step 13: Clean Up (Optional)

To remove the image:

```bash
docker rmi paraphrase-api
```

## Troubleshooting

### Container exits immediately
- Check logs: `docker logs paraphrase-api-container`
- Make sure the model file path is correct
- Verify the model file exists and is accessible

### Port already in use
- Change the port mapping: `-p 8001:8000` (use port 8001 instead)
- Or stop the service using port 8000

### Model not found
- Verify the volume mount path is correct
- Check file permissions
- Ensure the model file exists in your project directory

### Slow response
- This is normal - LLM inference takes time
- First request may be slower (model warmup)
- Subsequent requests should be faster

## Using Docker Compose (Alternative)

If you prefer using docker-compose:

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop:
```bash
docker-compose down
```

