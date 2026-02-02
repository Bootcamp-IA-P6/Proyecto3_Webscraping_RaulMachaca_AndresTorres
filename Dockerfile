FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

USER root
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ COPY TODO (incluye templates)
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml entrypoint.sh ./

# ✅ FIX: Crear directorios ANTES pip
RUN mkdir -p /app/data /app/reports/screenshots /var/log/cron && \
    touch /var/log/cron/scraper.log /var/log/cron.log && \
    chmod 777 /app/data /app/reports /var/log/cron/*

# ✅ CRÍTICO: Instalar Playwright browsers con PATH FIJO
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN pip install --no-cache-dir \
    requests beautifulsoup4 pydantic tomli jinja2 playwright==1.44.0 && \
    playwright install --with-deps chromium && \
    playwright install chromium

# ✅ FIX: Symlink para root user (cron ejecuta como root)
RUN mkdir -p /root/.cache/ms-playwright/chromium-1117/chrome-linux && \
    ln -sf /ms-playwright/chromium-*/chrome-linux/chrome /root/.cache/ms-playwright/chromium-1117/chrome-linux/chrome

# Cron setup
RUN echo "*/2 * * * * root cd /app && python -m src.game_scraper.main >> /var/log/cron/scraper.log 2>&1" > /etc/cron.d/game-scraper && \
    chmod 0644 /etc/cron.d/game-scraper

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
