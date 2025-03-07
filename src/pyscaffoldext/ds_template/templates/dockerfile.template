# Use a multi-stage build for efficiency
FROM python:3.12-slim-bookworm AS builder

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Install uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

# Set working directory
WORKDIR /app

# Copy only the dependency files needed for installation
COPY pyproject.toml uv.lock ./

# Install dependencies
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/opt/uv-cache/

RUN /root/.cargo/bin/uv sync --no-install-project --frozen

# Copy the rest of the application code
COPY . .

# Install the project
RUN /root/.cargo/bin/uv sync 

# Final stage
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Copy the installed dependencies and application from the builder stage
COPY --from=builder /app /app

# Set the PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "my_app"]