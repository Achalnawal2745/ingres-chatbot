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

# Copy application files
COPY . .

# Set up user with UID 1000 required for Hugging Face Spaces
RUN useradd -m -u 1000 user && \
    chown -R user:user /app
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=7860

EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "--workers", "1", "--threads", "4", "app:app"]
