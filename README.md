# Article Paraphrasing API

FastAPI service for paraphrasing articles using LLM while maintaining full length and all details.

## Features

- Paraphrase articles while preserving all information and length
- RESTful API with FastAPI
- Docker support for easy deployment
- Health check endpoints
- Statistics on paraphrasing quality

## API Endpoints

### `GET /`
Root endpoint - returns API status

### `GET /health`
Health check endpoint

### `POST /paraphrase`
Paraphrase an article

**Request Body:**
```json
{
  "article": "Your article text here...",
  "max_tokens": 3500
}
```

**Response:**
```json
{
  "original_article": "...",
  "paraphrased_article": "...",
  "statistics": {
    "original_word_count": 150,
    "paraphrased_word_count": 148,
    "length_match_percentage": 98.67,
    "inference_time_seconds": 25.5,
    "tokens_per_second": 5.8
  }
}
```

## Environment Variables

- `MODEL_PATH`: Path to the GGUF model file (default: `/app/models/llama-2-13b.Q4_K_M.gguf`)
- `N_CTX`: Context window size (default: 4096)
- `N_THREADS`: Number of threads (0 for auto-detect, default: 0)
- `N_BATCH`: Batch size for processing (default: 512)
- `PORT`: Server port (default: 8000)

## Docker Deployment

### Build the image:
```bash
docker build -t paraphrase-api .
```

### Run the container:
```bash
docker run -p 8000:8000 \
  -v /path/to/model:/app/models \
  -e MODEL_PATH=/app/models/llama-2-13b.Q4_K_M.gguf \
  paraphrase-api
```

## Coolify Deployment

1. Push your code to a Git repository
2. In Coolify, create a new application
3. Connect your repository
4. Coolify will automatically detect the Dockerfile
5. Set environment variables in Coolify dashboard
6. Mount the model file as a volume or upload it to the container

### Important Notes for Coolify:

- The model file (`llama-2-13b.Q4_K_M.gguf`) should be mounted as a volume or uploaded to the container
- Ensure sufficient resources (CPU, RAM) for the LLM model
- The model file is large (~7-8GB), so ensure adequate storage

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export MODEL_PATH=./llama-2-13b.Q4_K_M.gguf
export PORT=8000
```

3. Run the server:
```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

