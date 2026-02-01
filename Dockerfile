# GAME.es scraper + CRON cada 2 minutos
FROM python:3.12-slim

# Install cron + curl (mínimo)
RUN apt-get update && apt-get install -y \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml ./

# Create directories
RUN mkdir -p /app/data /var/log/cron && \
    chmod 777 /app/data /var/log/cron

# Install Python dependencies
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    pydantic \
    tomli

# Cronjob cada 2 minutos: */2 * * * *
RUN echo "*/2 * * * * root cd /app && python -m src.game_scraper.main >> /var/log/cron/scraper.log 2>&1" > /etc/cron.d/game-scraper

# Permissions
RUN chmod 0644 /etc/cron.d/game-scraper && \
    crontab /etc/cron.d/game-scraper

# Run cron foreground
CMD ["cron", "-f"]
