# --- Base Stage: Install Dependencies ---
FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS base

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install dependencies first (cached separately)
RUN uv pip install --system

# --- Final Stage: Copy Source Code ---
FROM base AS final

# Copy source code after dependencies are installed
COPY src/ /app/

# Set default command
CMD ["python", "-m", "arcdemo"]
