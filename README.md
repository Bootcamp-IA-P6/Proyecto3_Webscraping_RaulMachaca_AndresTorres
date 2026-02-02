# 📌 Step 2 — Docker Setup & Containerized Execution  
This section represents **Step 2** of the Game Scraper workflow.  
Here you will learn how to **containerize the scraper**, run it using **Docker Compose**, and verify that the output is correctly persisted.

---

# 🐳 Docker — Containerized Game Scraper

Docker allows you to run the scraper in a **clean, isolated environment**, without needing to install Python, uv, or dependencies on your machine.  
Everything runs inside a lightweight container based on **python:3.12-slim**.

---

# 🎮 Game Scraper Overview

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

# 🚀 Quick Start (Local Execution Recap)

Before using Docker, here is the local workflow (Step 1):

### Clone & Virtual Environment
```bash
git clone <repo> game-scraper
cd game-scraper

python -m venv venv
source venv/bin/activate      # Linux / Mac
# venv\Scripts\activate       # Windows
```

### uv setup (IMPORTANT)
```bash
pip install uv
uv sync --dev
uv pip install -e .
```

### Run scraper
```bash
uv run python -m src.game_scraper.main
```

### Run tests
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

# 🐳 Step 2 — Docker Setup & Usage  
Below is the **official Docker workflow** for running the scraper inside a container.

---

## ✅ 1. Quick Docker Run (recommended)
This command builds the image and starts the scraper:

```bash
docker-compose up --build
```

### ✔ What happens?
- Docker builds the image using `python:3.12-slim`
- Installs dependencies (`requests`, `beautifulsoup4`, etc.)
- Runs the scraper automatically
- Saves output files to:

```
data/products_*.json
data/products_*.csv
```

### ✔ Persistent Volume
Your local `./data` folder is mounted inside the container:

```
./data  →  /app/data
```

This means **files are saved on your machine**, not inside the container.

---

## 🧪 2. Single Run (one-time execution)
If you want to run the scraper once:

```bash
docker-compose run --rm game-scraper
```

---

## 📂 3. Verify Data Persistence
Check that the scraper generated files:

```bash
ls -la data/
```

You should see timestamped JSON and CSV files.

---

## 🧱 4. Docker Compose Services Breakdown
```bash
game-scraper:
  ✅ Image: python:3.12-slim (~150MB)
  ✅ Volume: ./data:/app/data (persistent)
  ✅ pip deps: requests + beautifulsoup4
  ✅ CMD: python -m src.game_scraper.main
```

### Explanation
| Component | Meaning |
|----------|---------|
| **Image** | Base container (lightweight Python 3.12) |
| **Volume** | Saves output to your local machine |
| **Dependencies** | Installed inside the container |
| **CMD** | Runs the scraper automatically |

---

## 🎯 Summary of Step 2

- You now have the scraper running **inside Docker**  
- Output files are saved **persistently**  
- No need to install Python or uv locally  
- Ready for **Step 3: Automated Cronjob Execution**

---
