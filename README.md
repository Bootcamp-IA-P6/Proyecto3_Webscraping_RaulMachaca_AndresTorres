# 📌 Step 3 — Cronjob Automation (every 2 minutes)  
Automated execution of the Game Scraper using a **cron-enabled Docker container**, generating timestamped JSON/CSV files every **2 minutes**.

---

# 🎮 Game Scraper

Professional **GAME.es** web scraper that extracts **Warhammer 40k** product data:

- Title, price, ratings, **related products** (007 First Light, GTA V)  
- **JSON + CSV** output with timestamps  
- **Pydantic** validation + **pytest** coverage  
- **uv** modern tooling  

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

# 🚀 Quick Start (Local Execution)

## Clone & Virtual Environment
```bash
git clone <repo> game-scraper
cd game-scraper
python -m venv venv
source venv/bin/activate      # Linux / Mac
# venv\Scripts\activate       # Windows
```

## uv setup (IMPORTANT)
```bash
pip install uv
uv sync --dev
uv pip install -e .
```

## Run scraper
```bash
uv run python -m src.game_scraper.main
```

## Run tests
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

### Alternative
```bash
PYTHONPATH=src pytest
```

---

# 🧠 Main Entrypoint
```
src/game_scraper/main.py
```

---

# 🐳 Docker (Step 2 Recap)

### Quick Docker Run
```bash
docker-compose up --build
# Files saved → data/products_*.json (persistent volume)
```

### Single Run
```bash
docker-compose run --rm game-scraper
```

### Verify Data Persistence
```bash
ls -la data/  # JSON + CSV files locally!
```

### Docker Compose Services
```bash
game-scraper:
  ✅ Image: python:3.12-slim (~150MB)
  ✅ Volume: ./data:/app/data (persistent)
  ✅ pip deps: requests + beautifulsoup4
  ✅ CMD: python -m src.game_scraper.main
```

---

# ⏰ Step 3 — Cronjob Automation (every 2 minutes)

The scraper can run **automatically every 2 minutes** using a cronjob inside the Docker container.

### What the cronjob does:
- Executes the scraper **every 2 minutes**  
- Generates timestamped **JSON + CSV** files  
- Saves them in a **persistent local volume**  
- Logs execution output  
- Fully compatible with **Windows Git Bash** using `MSYS_NO_PATHCONV=1`

---

# 🎯 Step 3 – Summary

### ✔ Cron runs the scraper every 2 minutes  
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

### ✔ Persistent volume works on Windows

---

# 🚀 Git Bash Commands (Windows)

## Start cron-enabled service
```bash
MSYS_NO_PATHCONV=1 docker-compose up -d --build
```

## View live logs (every 2 minutes)
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
Always run Docker Compose with:
```bash
MSYS_NO_PATHCONV=1 docker-compose up -d
```

### Direct Docker alternative
```bash
docker run -v "$(pwd)/data:/app/data"
```

---

# 📊 Step 3 Metrics

- Cron frequency: `*/2 * * * *`  
- Files generated: **720 per day**  
- Estimated size: ~50 KB per execution  
- Daily usage: ~36 MB  
- Storage: persistent local volume (`data/`)  

---
