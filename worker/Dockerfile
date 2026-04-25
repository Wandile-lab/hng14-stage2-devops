FROM python:3.12-slim

WORKDIR /app

# Create user safely
RUN id -u appuser || useradd -m appuser

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies FIRST (as root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Fix permissions BEFORE switching user
RUN chown -R appuser:appuser /app

# Drop privileges
USER appuser

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]
