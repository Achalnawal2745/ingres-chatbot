FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=10000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set up non-root user and assign permissions
RUN useradd -m -u 1000 user && \
    chown -R user:user /app

USER user

EXPOSE 10000

# Bind dynamically to Render's $PORT (defaults to 10000)
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-10000} --timeout 120 --workers 1 --threads 4 app:app"]
