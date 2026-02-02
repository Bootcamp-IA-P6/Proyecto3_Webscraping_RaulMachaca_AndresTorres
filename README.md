
Absolutely, Andrés — here is your **full README**, **in English**, **advanced Markdown**, **with table of contents**, and **preserving 100% of your original content** while keeping it clean, professional, and ready to paste directly into GitHub.

---

# 🎮 Game Scraper

Professional **GAME.es** web scraper that extracts **Warhammer 40k** product data:

- Title, price, ratings, **related products** (007 First Light, GTA V)  
- **JSON + CSV** output with timestamps  
- **Pydantic** validation + **pytest** coverage  
- **uv** modern tooling  

---

# 📚 Table of Contents

- [🎮 Game Scraper](#-game-scraper)
- [📊 Demo Output](#-demo-output)
- [🚀 Quick Start](#-quick-start)
  - [Clone & Virtual Environment](#clone--virtual-environment)
  - [uv Setup (IMPORTANT)](#uv-setup-important)
  - [Run Scraper](#run-scraper)
  - [Run Tests](#run-tests)
- [📁 Project Structure](#-project-structure)
- [🧪 Tests & Coverage](#-tests--coverage)
- [🔧 Troubleshooting (uv / pytest)](#-troubleshooting-uv--pytest)
- [🧠 Main Entrypoint](#-main-entrypoint)
- [🐳 Docker](#-docker)
  - [Quick Docker Run](#quick-docker-run)
  - [Single Run](#single-run)
  - [Verify Data Persistence](#verify-data-persistence)
  - [Docker Compose Services](#docker-compose-services)
- [⏰ Production Cronjob (every 2 minutes)](#-production-cronjob-every-2-minutes)
  - [Step 3 – Summary](#step-3--summary)
- [🪟 Git Bash Commands (Windows)](#-git-bash-commands-windows)
- [📁 docker-composeyml](#-docker-composeyml)
- [✅ Expected Output](#-expected-output)
- [🔧 Troubleshooting (Windows / Git Bash)](#-troubleshooting-windows--git-bash)
- [📊 Step 3 Metrics](#-step-3-metrics)

---

# 📊 Demo Output

**data/products_20260201_221200.json**
```json
{
  "title": "Warhammer 40.000 Space Marine II",
  "price": "34'99€",
  "ratings_count": "208 Valoraciones",
  "related_products": [
    { "name": "007 First Light", "price": "69'99€" },
    { "name": "Grand Theft Auto V", "price": "19'99€" }
  ]
}
```

---

# 🚀 Quick Start

## Clone & Virtual Environment
```bash
git clone <repo> game-scraper
cd game-scraper

python -m venv venv
source venv/bin/activate      # Linux / Mac
# venv\Scripts\activate       # Windows
```

---

## uv Setup (IMPORTANT)
```bash
pip install uv
uv sync --dev
uv pip install -e .
```

---

## Run Scraper
```bash
uv run python -m src.game_scraper.main
```

---

## Run Tests
```bash
uv run pytest tests/ -v
```

---

# 📁 Project Structure
```
src/game_scraper/     # Core scraper + parser
tests/                # pytest + HTML samples
data/                 # JSON + CSV output
config.toml           # GAME.es selectors
```

---

# 🧪 Tests & Coverage
```bash
uv run pytest --cov=src/game_scraper/ tests/
```

---

# 🔧 Troubleshooting (uv / pytest)

### Error
```
ModuleNotFoundError: No module named 'src'
```

### Solution
```bash
uv pip install -e .
```

### Alternative (run tests from ROOT)
```bash
PYTHONPATH=src pytest
```

---

# 🧠 Main Entrypoint
```
src/game_scraper/main.py
```

---

# 🐳 Docker

## Quick Docker Run
```bash
docker-compose up --build
# Files saved → data/products_*.json (persistent volume)
```

---

## Single Run
```bash
docker-compose run --rm game-scraper
```

---

## Verify Data Persistence
```bash
ls -la data/  # JSON + CSV files locally!
```

---

## Docker Compose Services
```bash
game-scraper:
  ✅ Image: python:3.12-slim (~150MB)
  ✅ Volume: ./data:/app/data (persistent)
  ✅ pip deps: requests + beautifulsoup4
  ✅ CMD: python -m src.game_scraper.main
```

---

# ⏰ Production Cronjob (every 2 minutes)

Cronjob configured to automatically run the scraper in production, generating persistent files every **2 minutes** using Docker.

- Automatic execution every 2 minutes  
- JSON + CSV files with timestamp  
- Logs accessible from Docker and inside the container  
- Windows + Git Bash compatible using `MSYS_NO_PATHCONV=1`  

---

## 🎯 Step 3 – Summary

### ✔ Cron runs scraper every 2 minutes  
### ✔ Generated files:
```
data/products_YYYYMMDD_HHMMSS.json
data/products_YYYYMMDD_HHMMSS.csv
```

### ✔ Logs available:
```
docker-compose logs -f
/var/log/cron/scraper.log
```

### ✔ Persistent volume (Windows compatible)

---

# 🪟 Git Bash Commands (Windows)

## Start (automatic cron)
```bash
MSYS_NO_PATHCONV=1 docker-compose up -d --build
```

## Live logs (every 2 minutes)
```bash
MSYS_NO_PATHCONV=1 docker-compose logs -f
```

## Stop service
```bash
MSYS_NO_PATHCONV=1 docker-compose down
```

## View generated files
```bash
ls -la data/      # Windows: dir data\
```

---

# 📁 docker-compose.yml
```bash
services:
  game-scraper:
    build: .
    container_name: game-scraper-cron
    volumes:
      - type: bind
        source: "./data"
        target: "/app/data"
    restart: unless-stopped
```

---

# ✅ Expected Output
```
data/products_20260202_013000.json
data/products_20260202_013000.csv
data/products_20260202_013200.json
data/products_20260202_013200.csv
```

All files are generated locally in the `data/` folder every 2 minutes.

---

# 🔧 Troubleshooting (Windows / Git Bash)

## Problem
A wrong folder named `data;C` is created.

## Solution
Always use:
```bash
MSYS_NO_PATHCONV=1 docker-compose up -d
```

### Direct Docker alternative
```bash
docker run -v "$(pwd)/data:/app/data"
```

---

# 📊 Step 3 Metrics

- Cron frequency: `*/2 * * * *` (every 2 minutes)  
- Files generated: **720 per day** (JSON + CSV)  
- Estimated size: ~50 KB per run  
- Daily usage: ~36 MB  
- Storage: persistent local volume (`data/`)  

