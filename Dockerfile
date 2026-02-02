FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml entrypoint.sh ./

RUN mkdir -p /app/data /var/log/cron && \
    touch /var/log/cron/scraper.log /var/log/cron.log && \
    chmod 777 /app/data /var/log/cron /var/log/cron/*

RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    pydantic \
    tomli \
    jinja2

# Cronjob cada 2 min + PATH completo
RUN echo "*/2 * * * * cd /app && /usr/local/bin/python -m src.game_scraper.main >> /var/log/cron/scraper.log 2>&1" > /etc/cron.d/game-scraper && \
    chmod 0644 /etc/cron.d/game-scraper && \
    crontab /etc/cron.d/game-scraper

ENTRYPOINT ["./entrypoint.sh"]