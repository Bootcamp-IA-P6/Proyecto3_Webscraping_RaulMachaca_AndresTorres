# Simple + reliable GAME.es scraper Docker
FROM python:3.12-slim

# Install only curl (minimum)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml ./

# Create data directory
RUN mkdir -p data && chmod 777 data

# Install Python dependencies with pip (SIMPLE)
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    pydantic \
    tomli

# Run scraper
CMD ["python", "-m", "src.game_scraper.main"]