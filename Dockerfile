# Stage 1: Builder
FROM --platform=linux/amd64 python:3.11-slim@sha256:7b5f29e90c05a6fa2c59d32eec8a058d1f2a87b1f2cf201b8b018a68c0a7f39b AS builder
WORKDIR /app

# Install non-root user early
RUN addgroup --system --gid 1000 appgroup && \
    adduser --system --uid 1000 --gid appgroup appuser

# Install system utilities for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Layer optimization: copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM --platform=linux/amd64 python:3.11-slim@sha256:7b5f29e90c05a6fa2c59d32eec8a058d1f2a87b1f2cf201b8b018a68c0a7f39b
WORKDIR /app

# Copy non-root user and system tools from builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /usr/bin/curl /usr/bin/curl
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code (bind mounts or copy)
COPY src/ ./src/
COPY examples/ ./examples/

# Switch to non-root user
USER appuser

# Expose port and set healthcheck
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "src/app.py"]
