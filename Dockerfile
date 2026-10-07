FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model during build so it does not download on runtime start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application files
COPY . .

# Pre-ingest Chroma documents during image build so startup is instant
RUN python -c "from rag_pipeline import ingest_documents; ingest_documents()" || true

# Set up non-root user and assign permissions
RUN useradd -m -u 1000 user && \
    chown -R user:user /app /home/user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=10000

EXPOSE 10000

# Bind dynamically to Render's $PORT (defaults to 10000)
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-10000} --timeout 180 --workers 1 --threads 4 app:app"]
