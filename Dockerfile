# Multi-stage build: minimal + production
FROM python:3.12-slim AS builder

# Install uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.cargo/bin/uv --version

WORKDIR /app
COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/uv \
    /root/.cargo/bin/uv pip install --cache-dir /root/.cache/uv -e .

FROM python:3.12-slim AS runtime
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy uv + installed packages
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
RUN mkdir -p data

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uv", "run", "python", "-m", "src.game_scraper.main"]
