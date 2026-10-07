FROM python:3.10-slim

WORKDIR /app

ENV HF_HOME=/app/.cache \
    TRANSFORMERS_CACHE=/app/.cache \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model during build into /app/.cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application files
COPY . .

# Pre-build vector database during Docker build so it is 100% ready before starting
RUN python -c "from rag_pipeline import ingest_documents; ingest_documents(max_pages=50)" || true

# Set up non-root user and assign permissions
RUN useradd -m -u 1000 user && \
    chown -R user:user /app /home/user

USER user

EXPOSE 10000

# Bind dynamically to Render's $PORT (defaults to 10000)
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-10000} --timeout 180 --workers 1 --threads 4 app:app"]
