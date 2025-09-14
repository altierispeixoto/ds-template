# syntax=docker/dockerfile:1.4

# Use a multi-stage build for efficiency
FROM python:3.12-slim-bookworm AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/opt/uv-cache/

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv using official install script
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# Create non-root user
RUN useradd -m -s /bin/bash app-user

# Set working directory and ownership
WORKDIR /app
RUN chown app-user:app-user /app

# Switch to non-root user
USER app-user

# Copy dependency files with explicit ownership
COPY --chown=app-user:app-user pyproject.toml uv.lock ./

# Install dependencies using mount cache
RUN --mount=type=cache,target=/opt/uv-cache,uid=$(id -u app-user) \
    /root/.cargo/bin/uv sync --no-install-project --frozen

# Copy the rest of the application code
COPY --chown=app-user:app-user . .

# Final stage
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -s /bin/bash app-user

# Set working directory and ownership
WORKDIR /app
RUN chown app-user:app-user /app

# Copy the installed dependencies and application from the builder stage
COPY --from=builder --chown=app-user:app-user /app /app

# Switch to non-root user
USER app-user

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Default command
ENTRYPOINT ["uv", "run"]
CMD ["my_app"]