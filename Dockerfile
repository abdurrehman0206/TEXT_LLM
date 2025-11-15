# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p /app/models

# Download the model from Hugging Face during build
# Using huggingface-cli which comes with huggingface-hub package
RUN huggingface-cli download TheBloke/Llama-2-13B-GGUF llama-2-13b.Q4_K_M.gguf --local-dir /app/models --local-dir-use-symlinks False

# Copy application code
COPY main.py .
COPY paraphrase_service.py .

# Expose port
EXPOSE 8000

# Set environment variables
ENV MODEL_PATH=/app/models/llama-2-13b.Q4_K_M.gguf
ENV N_CTX=4096
ENV N_THREADS=0
ENV N_BATCH=512
ENV PORT=8000

# Health check (using curl if available, otherwise skip)
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

