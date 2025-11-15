from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager
import os
from paraphrase_service import ParaphraseService

# Initialize the paraphrase service
# Try to find model file: check environment variable, then current directory, then Docker path
def get_model_path():
    """Get the model path, checking multiple locations"""
    # First check environment variable
    env_path = os.getenv("MODEL_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # Check current directory (for local development)
    current_dir_model = os.path.join(os.getcwd(), "llama-2-13b.Q4_K_M.gguf")
    if os.path.exists(current_dir_model):
        return current_dir_model
    
    # Check Docker path
    docker_path = "/app/models/llama-2-13b.Q4_K_M.gguf"
    if os.path.exists(docker_path):
        return docker_path
    
    # Return the first available option or default
    return env_path or current_dir_model or docker_path

MODEL_PATH = get_model_path()
N_CTX = int(os.getenv("N_CTX", "4096"))
N_THREADS = int(os.getenv("N_THREADS", "0")) or None  # 0 means auto-detect
N_BATCH = int(os.getenv("N_BATCH", "512"))

paraphrase_service: Optional[ParaphraseService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    global paraphrase_service
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        print(f"Loading model from {MODEL_PATH}...")
        paraphrase_service = ParaphraseService(
            model_path=MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            n_batch=N_BATCH
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise
    
    yield
    
    # Shutdown (if needed)
    paraphrase_service = None


app = FastAPI(
    title="Article Paraphrasing API",
    description="API for paraphrasing articles using LLM while maintaining full length and details",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParaphraseRequest(BaseModel):
    """Request model for paraphrasing"""
    article: str = Field(..., description="The original article text to paraphrase", min_length=10)
    max_tokens: Optional[int] = Field(3500, description="Maximum tokens to generate", ge=100, le=8000)


class ParaphraseResponse(BaseModel):
    """Response model for paraphrasing"""
    original_article: str
    paraphrased_article: str
    statistics: dict


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Article Paraphrasing API",
        "status": "running",
        "model_loaded": paraphrase_service is not None
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": paraphrase_service is not None
    }


@app.post("/paraphrase", response_model=ParaphraseResponse)
async def paraphrase_article(request: ParaphraseRequest):
    """
    Paraphrase an article while maintaining full length and all details
    
    Args:
        request: ParaphraseRequest containing the article and optional parameters
        
    Returns:
        ParaphraseResponse with paraphrased article and statistics
    """
    if paraphrase_service is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check server logs.")
    
    if not request.article or len(request.article.strip()) < 10:
        raise HTTPException(status_code=400, detail="Article must be at least 10 characters long")
    
    try:
        result = paraphrase_service.paraphrase_article(
            original_article=request.article,
            max_tokens=request.max_tokens
        )
        return ParaphraseResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error paraphrasing article: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

