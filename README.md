# Game Scraper

Professional **GAME.es** web scraper that extracts **Warhammer 40k** product data:

- Title, price, ratings, **related products** (007 First Light, GTA V)
- **JSON + CSV** output with timestamps
- **Pydantic** validation + **pytest** coverage
- **uv** modern tooling

---

## 🎮 Demo Output

**data/products_20260201_221200.json**

{
  "title": "Warhammer 40.000 Space Marine II",
  "price": "34'99€",
  "ratings_count": "208 Valoraciones",
  "related_products": [
    { "name": "007 First Light", "price": "69'99€" },
    { "name": "Grand Theft Auto V", "price": "19'99€" }
  ]
}

---

## 🚀 Quick Start
## Clone & Virtual Environment

git clone <repo> game-scraper
cd game-scraper
python -m venv venv
source venv/bin/activate   # Linux / Mac
.# venv\Scripts\activate    # Windows

## uv setup (IMPORTANT)

pip install uv
uv sync --dev
uv pip install -e .

## Run scraper

uv run python -m src.game_scraper.main

## Run tests

uv run pytest tests/ -v

# 📁 Project Structure

src/game_scraper/     # Core scraper + parser
tests/               # pytest + HTML samples
data/                # JSON + CSV output
config.toml          # GAME.es selectors

## 🧪 Tests & Coverage

uv run pytest --cov=src/game_scraper/ tests/

# 🔧 Troubleshooting (uv / pytest)

## Error:
ModuleNotFoundError: No module named 'src'

## Solution:
uv pip install -e .

## Alternative (run tests from ROOT):
PYTHONPATH=src pytest

# 🧠 Main Entrypoint

src/game_scraper/main.py

